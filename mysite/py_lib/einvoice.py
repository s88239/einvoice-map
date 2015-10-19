import string
import time, datetime, calendar
import random
import math
import itertools

import base64
import hmac
import hashlib
import urllib
import json

from http.cookiejar import CookieJar
try:
	from py_lib.invoice import Invoice
	from py_lib.seller import *
except:
	from invoice import Invoice
	from seller import *

def uniqid(prefix='', more_entropy=False):
	m = time.time()
	uniqid = '%8x%05x' %(math.floor(m),(m-math.floor(m))*1000000)
	if more_entropy:
		valid_chars = list(set(string.hexdigits.lower()))
		entropy_string = ''
		for i in range(0,10,1):
			entropy_string += random.choice(valid_chars)
		uniqid = uniqid + entropy_string
	uniqid = prefix + uniqid
	return uniqid

def dict_sort(d):
	return [(k,d[k]) for k in sorted(d.keys())]

def get_param_list(param_dict):
	param_list = ""
	encode_param_list = ""
	for key, value in param_dict:
		param_list += key + "=" + value + "&"
		encode_param_list += key + "=" + urllib.parse.quote_plus(value) + "&"
	param_list = param_list[:len(param_list)-1]
	encode_param_list = encode_param_list[:len(encode_param_list)-1]
	return param_list,encode_param_list

def url_parameter(api_key, param_dict):
	param_dict = dict_sort(param_dict)
	[param_list,encode_param_list] = get_param_list(param_dict)
	signature = hmac.new(api_key.encode('utf-8'), param_list.encode('utf-8'), hashlib.sha1).digest()
	signature = base64.b64encode(signature)
	return(encode_param_list, signature)

def get_url_json(query_url):
	req = urllib.request.Request(query_url, None, {'User-Agent': 'Mozilla/5.0 (X11; Linux i686; G518Rco3Yp0uLV40Lcc9hAzC1BOROTJADjicLjOmlr4=) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36','Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8','Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3','Accept-Encoding': 'gzip, deflate, sdch','Accept-Language': 'en-US,en;q=0.8','Connection': 'keep-alive'})
	cj = CookieJar()
	opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
	with opener.open(req) as url:
		data = json.loads(url.read().decode())
	return data

def carrier_query(user):
	data = {}
	count = 0
	while "code" not in data or data["code"] != 200:
		param_dict = {}
		param_dict["version"] = "1.0"
		param_dict["serial"] = "0000000001"
		param_dict["action"] = "qryCarrierAgg"
		param_dict["cardType"] = user.card_type
		param_dict["cardNo"] = user.card_no
		param_dict["cardEncrypt"] = user.card_encrypt
		param_dict["appID"] = user.app_id
		param_dict["timeStamp"] = str(int(time.time())+10)
		param_dict["uuid"] = uniqid()

		(param_list, signature) = url_parameter(user.api_key, param_dict)
		carrier_query_url = 'https://www.einvoice.nat.gov.tw/PB2CAPIVAN/Carrier/Aggregate?' + param_list + '&signature=' + signature.decode()

		data = get_url_json(carrier_query_url)

		if count > 10:
			break
		count += 1

	# for carrier_property in data["carriers"]:
	# 	print(carrier_property)

	return count, data["carriers"]

def invoice_header_query(user, start_date, end_date):
	invoice_list = []
	# now = datetime.datetime.now()
	# year = now.year
	# for year in range(now.year-1, now.year+1):
	# 	for month in range(1, 13):
	# 		if year >= now.year and month > now.month:
	# 			break
	# 		start_date = "{0:0=4d}".format(year) + "/" + "{0:0=2d}".format(month) + "/" + "01"
	# 		end_date = "{0:0=4d}".format(year) + "/" + "{0:0=2d}".format(month) + "/" + "{0:0=2d}".format(calendar.monthrange(year, month)[1])
			
	data = {}
	while "code" not in data or data["code"] != 200:
		param_dict = {}
		param_dict["version"] = "0.2"
		param_dict["action"] = "carrierInvChk"
		param_dict["cardType"] = user.card_type
		param_dict["cardNo"] = user.card_no
		param_dict["cardEncrypt"] = user.card_encrypt
		param_dict["appID"] = user.app_id
		param_dict["timeStamp"] = str(int(time.time())+10)
		param_dict["expTimeStamp"] = str(int(time.time())+1000)
		param_dict["startDate"] = start_date
		param_dict["endDate"] =  end_date				
		param_dict["onlyWinningInv"] = "N"
		param_dict["uuid"] = uniqid()
	
		(param_list, signature) = url_parameter(user.api_key, param_dict)
		invoice_header_url = 'https://www.einvoice.nat.gov.tw/PB2CAPIVAN/invServ/InvServ?' + param_list + '&signature=' + signature.decode()
		data = get_url_json(invoice_header_url)

		if data["code"] == 903:
			break

		for inv in data["details"]:
			if "sellerName" in inv:
				new_invoice = Invoice(inv)
				#new_invoice.inv_num = str(filter(lambda x: x in string.printable, new_invoice.inv_num))
				check = True
				for invoice in invoice_list:
					if new_invoice.inv_num == invoice.inv_num:
						check = False
						break
				if check:
					invoice_list.append(new_invoice)
	return invoice_list

def invoice_item_query(user, invoice_list):
	for inv, i in zip(invoice_list, itertools.count()):
		data = {}
		while "code" not in data or data["code"] != 200:
			param_dict = {}
			param_dict["version"] = "0.1"
			param_dict["action"] = "carrierInvDetail"
			param_dict["cardType"] = user.card_type
			param_dict["cardNo"] = user.card_no
			param_dict["cardEncrypt"] = user.card_encrypt
			param_dict["appID"] = user.app_id
			param_dict["timeStamp"] = str(int(time.time())+10)
			param_dict["expTimeStamp"] = str(int(time.time())+1000)
			param_dict["uuid"] = uniqid()
			param_dict["invNum"] = inv.inv_num
			param_dict["invDate"] = "{0:0=4d}/{1:0=2d}/{2:0=2d}".format((inv.inv_date.year+1911), inv.inv_date.month, inv.inv_date.day)
			param_dict["sellerName"] = urllib.parse.quote(inv.seller_name)
			param_dict["amount"] = str(inv.amount)

			(param_list, signature) = url_parameter(user.api_key, param_dict)
			invoice_item_url = 'https://www.einvoice.nat.gov.tw/PB2CAPIVAN/invServ/InvServ?' + param_list + '&signature=' + signature.decode()
			data = get_url_json(invoice_item_url)
			if "details" in data:	
				for item in data["details"]:
					invoice_list[i].add_item(item) 
	return invoice_list

def get_einvoice(user, start_date, end_date, all_sellers):
	invoice_list = invoice_header_query(user, start_date, end_date)
	invoice_list = invoice_item_query(user, invoice_list)
	for inv in invoice_list:
		inv.add_carrier_name(user)	
		#for key, value in all_sellers.items():
		#	(cur_store_name, cur_branch_name) = split_store_and_branch(inv.seller_name)	
		#	if value.branch_name == cur_branch_name and (cur_store_name=='' and test_store_name(value.store_name) or cur_store_name[:2] == value.store_name[:2]):
		#		inv.add_seller(value)
		#		break
		#if inv.seller == None:
		#	inv.add_seller(Seller(-1, inv.seller_name, '', 0, 0))
	return invoice_list

# def login(account, password):
# 	#TEST
# 	api_key = "QWQ4dU9WMzRXa2xoYUdsZA=="
# 	app_id = "EINV0201505042102"
# 	card_type = "3J0002"
# 	card_no = account #"/SMV1EFQ"
# 	card_encrypt = password #"1212"

# 	invoice_list = get_einvoice(api_key, app_id, card_type, card_no, card_encrypt)
# 	return invoice_list

if __name__ == '__main__':
	api_key = "QWQ4dU9WMzRXa2xoYUdsZA=="
	app_id = "EINV0201505042102"
	card_type = "3J0002"
	card_no = "/SMV1EFQ"
	card_encrypt = "1212"

	# invoice_list = get_einvoice(api_key, app_id, card_type, card_no, card_encrypt)
	# carrier_query(api_key, app_id, card_type, card_no, card_encrypt)
	# import pickle
	# with open('invoice_list_tmp.pkl', 'wb') as f:
	# 	pickle.dump(invoice_list, f)
	# for i in invoice_list:
	# 	i._print()
