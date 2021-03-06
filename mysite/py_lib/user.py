import sys
import os

import time, datetime, calendar
try:
	import py_lib.einvoice as einvoice
	from py_lib.seller import *
	from py_lib.invoice import *
	from trips.models import *
	from django.db import IntegrityError
except:
	from invoice import * 
	import pickle
	import einvoice
	from seller import *

'''if sys.version_info >= (2, 7, 9):
	import ssl
	ssl._create_default_https_context = ssl._create_unverified_context'''
TEST =  False
class User(object):
	not_item_list = ['折扣', '折抵', '滿額送', '抵用券', '紅利贈送', '任選第2件', '39元超值組合', '49元超值組合']

	def __init__(self, api_key, app_id, card_type, card_no, card_encrypt, all_sellers):
		self.api_key = api_key
		self.app_id = app_id
		self.card_type = card_type
		self.card_no = card_no
		self.card_encrypt = card_encrypt

		self.carriers = einvoice.carrier_query(self)
		if self.carriers==False:
			return
		self.invoice_list, self.invoices_to_database = self.get_invoice_list(all_sellers)
		self.seller_to_invoice(all_sellers)		

		#key is the id of seller
		self.sellers = {}

		#key is the seller_name in invoice
		self.visit_frequency = {}
		self.top_item = {} #value is(item_description, quantity)
		self.all_items = {} #for top_item
		self.consumption = {}

		self.seller_not_on_csv = []
	
	def seller_to_invoice(self, all_sellers):
		for inv in self.invoice_list:
			for key, value in all_sellers.items():
				if match_seller(inv.seller_name, value):
					inv.add_seller(value)
					break
			if inv.seller == None:
				inv.add_seller(Seller(-1, inv.seller_name, '', 0, 0))


	def get_invoice_list(self, all_sellers):
		invoice_list = []
		invoices_from_database = InvoiceTable.objects.filter(card_no = self.card_no)
		for carrier in self.carriers:
			invoices_from_database = invoices_from_database | InvoiceTable.objects.filter(card_no=carrier['carrierId2'])
		now = datetime.datetime.now()
		for invoice in invoices_from_database:
			details = {}
			details['invNum'] = invoice.inv_num
			details['cardType'] = invoice.card_type
			details['cardNo'] = invoice.card_no
			details['sellerName'] = invoice.seller_name
			details['amount'] = invoice.amount
			details['invPeriod']= invoice.inv_preiod
			details['invStatus']= invoice.inv_status
			details['invDonatable']= invoice.inv_donatable
			details['donateMark']= invoice.donate_mark

			date_details = {}
			date_details['year'] = invoice.inv_date.split('/')[0]
			date_details['month'] = invoice.inv_date.split('/')[1]
			date_details['date'] = invoice.inv_date.split('/')[2]
			details['invDate'] = date_details

			inv_items = invoice.inv_items.split('|')
			carrier_name = invoice.carrier_name			

			invoice = Invoice(details)
			invoice.carrier_name = carrier_name
			
			i = 0
			while i < len(inv_items):
				item = {}
				item['rowNum'] = inv_items[i]
				item['description'] = inv_items[i+1]
				item['quantity'] = inv_items[i+2]
				item['unitPrice'] = inv_items[i+3]
				item['amount'] = inv_items[i+4]
				i += 5				
				invoice.add_item(item)
			
			invoice_list.append(invoice)
		if len(invoices_from_database) == 0:
			for year in range(now.year-1, now.year+1):
				for month in range(1, 13):
					if year >= now.year and month > now.month:
						break
					(start_date, end_date) = self.date_for_query(year, month)
					invoice_list.extend(einvoice.get_einvoice(self, start_date, end_date, all_sellers))
		else:
			latest_date = sorted(invoices_from_database, key=lambda x: x.inv_date, reverse=True)[0].inv_date
			YMD = latest_date.split('/')

			query_start_date = datetime.date(int(YMD[0])+1911, int(YMD[1]), int(YMD[2]))
			for year in range(query_start_date.year, now.year+1):
				if (year == query_start_date.year) and (year < now.year): 
					for month in range(query_start_date.month, 13):
						(start_date, end_date) = self.date_for_query(year, month)
						invoice_list.extend(einvoice.get_einvoice(self, start_date, end_date, all_sellers))
				elif (year > query_start_date.year) and (year < now.year):
					for month in range(1,13):
						(start_date, end_date) = self.date_for_query(year, month)
						invoice_list.extend(einvoice.get_einvoice(self, start_date, end_date, all_sellers))
				elif (year == now.year) and (year == query_start_date.year):
					for month in range(query_start_date.month, now.month+1):
						(start_date, end_date) = self.date_for_query(year, month)
						invoice_list.extend(einvoice.get_einvoice(self, start_date, end_date, all_sellers))
				elif (year == now.year) and (year > query_start_date.year):
					for month in range(1, now.month+1):
						(start_date, end_date) = self.date_for_query(year, month)
						invoice_list.extend(einvoice.get_einvoice(self, start_date, end_date, all_sellers))
		
		return self.get_unique_inv_list(invoice_list, invoices_from_database)

	def get_unique_inv_list(self, invoice_list, invoices_from_database):
		inv_nums_in_database = set()
		invoices_to_database = []
		for ele in invoices_from_database:
			inv_nums_in_database.add(ele.inv_num)
		
		inv_nums = {}
		for ele in invoice_list:
			inv_nums[ele.inv_num] = ele
		invoice_list = inv_nums.values()

		for ele in invoice_list:
			if ele.inv_num not in inv_nums_in_database:
				invoices_to_database.append(ele)
		return invoice_list, invoices_to_database

	def date_for_query(self, year, month):
		start_date = "{0:0=4d}".format(year) + "/" + "{0:0=2d}".format(month) + "/" + "01"
		end_date = "{0:0=4d}".format(year) + "/" + "{0:0=2d}".format(month) + "/" + "{0:0=2d}".format(calendar.monthrange(year, month)[1])
		return (start_date, end_date)

	def str_carriers(self):
		carriers_str = ''
		for ele in self.carriers:
			carriers_str +=	ele['carrierId2'] + ' '
		return carriers_str.strip()

	def str_items(self, items):
		items_str = ''
		for ele in items:
			items_str += ele.__str__() + '|'
		return items_str[:-1]

	def str_invoice_num(self):
		invoice_num_str = ''
		for ele in self.invoice_list:
			invoice_num_str += ele.inv_num + ' '
		return invoice_num_str.strip()
	
	def store_unmatchseller(self):
		for ele in self.seller_not_on_csv:
			try:
				data = UnMatchSellerTable.objects.get(seller_name = ele)
			except:
				data= UnMatchSellerTable.objects.create( seller_name =ele )
				data.save()
	
	def store_invoice_database(self):
		for invoice in self.invoices_to_database:
			data = InvoiceTable.objects.create(inv_num=invoice.inv_num,
				card_type=invoice.card_type,
				card_no=invoice.card_no,
				carrier_name=invoice.carrier_name,
				seller_name=invoice.seller_name,
				amount=invoice.amount,
				inv_date=invoice.inv_date.__str__(),
				inv_preiod=invoice.inv_period,
				inv_status=invoice.inv_status,
				inv_donatable=invoice.inv_donatable,
				donate_mark=invoice.donate_mark,
				inv_items=self.str_items(invoice.item))
			try:
				data.save()
			except IntegrityError as e:
				print('fuck')

	def store_carrier_database(self):
		for ele in self.carriers:
			carrier_from_database =  CarrierTable.objects.filter(carrier_id = ele['carrierId2'])
			if len(carrier_from_database) == 0:
				data = CarrierTable.objects.create(
					carrier_type = ele['carrierType'],
					carrier_id = ele['carrierId2'],
					carrier_name = ele['carrierName']
					)
				data.save()

	def store_user_database(self):
		try:
			_user = UserTable.objects.get(card_no = self.card_no)
		except:
			_user = UserTable.objects.create(api_key=self.api_key, 
					app_id=self.app_id, 
					card_type=self.card_type, 
					card_no=self.card_no, 
					card_encrypt=self.card_encrypt, 
					carriers_keys=self.str_carriers(), 
					invoice_keys=self.str_invoice_num())
			_user.save()
		_user.carriers_keys = self.str_carriers()
		_user.save()

	def add_seller(self, s, key_name):
		self.sellers[s.id] = Seller(s.id, s.store_name, s.address, s.longitude, s.latitude)
		self.sellers[s.id].set_branch_name(s.branch_name)
		self.sellers[s.id].set_visit_frequency(self.visit_frequency[key_name])
		self.sellers[s.id].set_consumption(self.consumption[key_name])
		if len(self.top_item[key_name]) == 0:
			return
		self.sellers[s.id].set_top_item(self.top_item[key_name][0])

	def sort_inv_list(self, by_date=True):
		if by_date:
			return sorted(self.invoice_list, key=lambda inv: inv.inv_date.getDate())

	def sort_inv_list_in_sellers(self, by_date=True):
		if by_date:
			for key in self.sellers:
				self.sellers[key].invoice_list = sorted(self.sellers[key].invoice_list, key=lambda inv: inv.inv_date.getDate(), reverse=True)

	def statistics(self, all_sellers):
		def is_item(item):
			for not_item in User.not_item_list:
				if item.description.find(not_item) != -1:
					return False
				if float(item.unitPrice) <= 0 and float(item.amount) <= 0:
					return False
			return True

		tmp_invoice_list = {}
		for invoice in self.invoice_list:
			if invoice.seller_name not in self.visit_frequency:
				self.visit_frequency[invoice.seller_name] = 0
				self.all_items[invoice.seller_name] = {}
				self.consumption[invoice.seller_name] = 0.0
			if invoice.seller_name not in tmp_invoice_list:
				tmp_invoice_list[invoice.seller_name] = []
			tmp_invoice_list[invoice.seller_name].append(invoice)
			self.visit_frequency[invoice.seller_name] += 1
			for item in invoice.item:
				if not is_item(item):
					continue
				if item.description not in self.all_items[invoice.seller_name]:
					self.all_items[invoice.seller_name][item.description] = 0
				self.all_items[invoice.seller_name][item.description] += float(item.quantity)
			self.consumption[invoice.seller_name] += float(invoice.amount)

		for i in self.all_items:
			top = 0  
			for j in self.all_items[i]:
				if top < self.all_items[i][j]:
					top = self.all_items[i][j]
			self.top_item[i] = [] 
			for j in self.all_items[i]:
				if self.all_items[i][j] >= top:
					self.top_item[i].append( (j, self.all_items[i][j]) )

		for seller_name in self.visit_frequency:
			seller_on_csv = False
			for csv_seller_key in all_sellers:
				if match_seller(seller_name, all_sellers[csv_seller_key]):
					self.add_seller(all_sellers[csv_seller_key],seller_name)
					self.sellers[all_sellers[csv_seller_key].id].invoice_list = tmp_invoice_list[seller_name]
					seller_on_csv = True
			if not seller_on_csv:
				self.seller_not_on_csv.append(seller_name)


def clustering(user):
	if len(user) <= 3:
		i = 0
		longitude = 121.516946
		latitude = 25.047941
		for key in user.keys():
			longitude = user[key].longitude
			latitude = user[key].latitude
			user[key].cluster = i
			i = i+1
		return user, user.keys(), (longitude, latitude)
	import numpy as np
	from sklearn.cluster import MeanShift, estimate_bandwidth
	from sklearn.datasets.samples_generator import make_blobs
	X = []
	numbers = []
	'''for number in user:
		X.append([user.longitude, user.latitde])
		numbers.append(number)'''

	for key, value in user.items():
		X.append([float(value.longitude),float(value.latitude)])
		numbers.append(key)
	# Compute clustering with MeanShift
	ms = MeanShift()
	ms.fit(X)
	labels = ms.labels_
	# fill in the predict labels
	for i in range(len(labels)):
		user[ numbers[i] ].cluster = labels[i]

	# find the biggest cluster
	biggest_cluster = max(set(labels), key=list(labels).count)
	cluster_centers = ms.cluster_centers_
	biggest_cluster_center = cluster_centers[biggest_cluster]

	labels_unique = np.unique(labels)
	n_clusters_ = len(labels_unique)


	return user, sorted(user, key=lambda x:user[x].cluster), (biggest_cluster_center[0], biggest_cluster_center[1])

def login(account, password):
	csv = os.path.join(os.path.dirname(os.path.dirname(__file__)),'static','Taipei_shops_with_einvoice.csv')
	all_sellers = list_sellers(csv)
	
	api_key = "QWQ4dU9WMzRXa2xoYUdsZA=="
	app_id = "EINV0201505042102"
	card_type = "3J0002"
	card_no = account
	card_encrypt = password
	user = User(api_key, app_id, card_type, card_no, card_encrypt, all_sellers)
	if user.carriers==False:
		return False

	user.statistics(all_sellers)
	user.sort_inv_list_in_sellers()
	user.store_user_database()
	user.store_carrier_database()
	user.store_invoice_database()
	user.store_unmatchseller()

	(sellers, sorted_key, center) = clustering(user.sellers)
	return sellers,sorted_key, user.sort_inv_list(), center

if __name__ == '__main__':
	TEST = True
	api_key = "QWQ4dU9WMzRXa2xoYUdsZA=="
	app_id = "EINV0201505042102"
	card_type = "3J0002"
	card_no = ''
	card_encrypt = ''
	user = User(api_key, app_id, card_type, card_no, card_encrypt)
	csv = os.path.join('..','static','Taipei_shops_with_einvoice.csv')
	all_sellers1 = list_sellers(csv)	

	user.statistics(csv)

