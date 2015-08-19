import sys
import os

import time, datetime, calendar
try:
	import py_lib.einvoice as einvoice
	from py_lib.seller import list_sellers
	from py_lib.seller import Seller
	from py_lib.invoice import *
	from py_lib.seller import split_store_and_branch
	from py_lib.seller import test_store_name
	from trips.models import *
except:
	from invoice import * 
	import pickle
	import einvoice
	from seller import list_sellers
	from seller import Seller
	from seller import split_store_and_branch
	from seller import test_store_name

'''if sys.version_info >= (2, 7, 9):
	import ssl
	ssl._create_default_https_context = ssl._create_unverified_context'''
TEST =  False
class User(object):
	not_item_list = ['折扣', '折抵', '滿額送', '抵用券', '紅利贈送', '任選第2件', '39元超值組合']

	def __init__(self, api_key, app_id, card_type, card_no, card_encrypt):
		self.api_key = api_key
		self.app_id = app_id
		self.card_type = card_type
		self.card_no = card_no
		self.card_encrypt = card_encrypt


		self.carriers = einvoice.carrier_query(api_key, app_id, card_type, card_no, card_encrypt)
		self.invoice_list = get_invoice_list()
		# if not TEST:
		# 	self.invoice_list = einvoice.get_einvoice(api_key, app_id, card_type, card_no, card_encrypt)
		# else:
		# 	with open('invoice_list_tmp.pkl', 'rb') as f:
		# 		self.invoice_list = pickle.load(f)


		#key is the id of seller
		self.sellers = {}

		#key is the seller_name in invoice
		self.visit_frequency = {}
		self.top_item = {} #value is(item_description, quantity)
		self.all_items = {} #for top_item
		self.consumption = {}

		self.seller_not_on_csv = []


	def get_invoice_list(self):
		invoice_list = []

		invoices_from_database = InvoiceTable.objects.filter(card_no = self.card_no)
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
			details['doanteMark']= invoice.donate_mark

			date_details = {}
			date_details['year'] = invoice.inv_date.split('/')[0]
			date_details['month'] = invoice.inv_date.split('/')[1]
			date_details['date'] = invoice.inv_date.split('/')[2]
			details['invDate'] = date_details

			inv_items = invoice.inv_items.split()
			invoice = Invoice(details)
			i = 0
			while i < len(inv_items):
				item = {}
				item['rowNum'] = inv_items[i]
				item['description'] = inv_items[i+1]
				item['quantity'] = inv_items[i+2]
				item['unitPrice'] = inv_items[i+3]
				item['amount'] = inv_items[i+4]
				i += 5				
				invoice.add_item(Item(item))

			invoice_list.append(invoice)

		if invoices_from_database == []:
			for year in range(now.year-1, now.year+1):
				for month in range(1, 13):
					if year >= now.year and month > now.month:
						break
					(start_date, end_date) = date_for_query(year, month)
					invoice_list.extend(einvoice.get_einvoice(self, start_date, end_date))
		else:
			latest_date = sorted(invoices_from_database, key=lambda x: x.inv_date, reverse=True)[0].inv_date
			YMD = latest_date.split('/')
			#start_date = '/'.join([int(YMD[0])+1911, YMD[1:]])
			#end_date = "{0:0=4d}".format(now.year) + "/" + "{0:0=2d}".format(now.month) + "/" + "{0:0=2d}".format(now.day)

			start_date = datetime.date(int(YMD[0])+1911, int(YMD[1]), int(YMD[2]))

			for year in range(start_date.year, now.year+1):
				if (year == start_date.year) and (year < now.year): 
					for month in range(start_date.month, 13):
						(start_date, end_date) = date_for_query(year, month)
						invoice_list.extend(einvoice.get_einvoice(self, start_date, end_date))
				elif (year > start_date.year) and (year < now.year):
					for month in range(1,13):
						(start_date, end_date) = date_for_query(year, month)
						invoice_list.extend(einvoice.get_einvoice(self, start_date, end_date))
				elif (year == now.year) and (year == start_date.year):
					for month in range(start_date.month, now.month+1):
						(start_date, end_date) = date_for_query(year, month)
						invoice_list.extend(einvoice.get_einvoice(self, start_date, end_date))
				elif (year == now.year) and (year > start_date.year):
					for month in range(1, now.month+1):
						(start_date, end_date) = date_for_query(year, month)
						invoice_list.extend(einvoice.get_einvoice(self, start_date, end_date))

		return get_unique_inv_list(invoice_list)

	def get_unique_inv_list(self, invoice_list):
		inv_nums = set()
		for ele in invoice_list:
			if ele.inv_num in inv_nums:
				invoice_list.remove(ele)
			else:
				inv_nums.add(ele.inv_num)
		return invoice_list

	def date_for_query(self, year, month):
		start_date = "{0:0=4d}".format(year) + "/" + "{0:0=2d}".format(month) + "/" + "01"
		end_date = "{0:0=4d}".format(year) + "/" + "{0:0=2d}".format(month) + "/" + "{0:0=2d}".format(calendar.monthrange(year, month)[1])
		return (start_date, end_date)

	def str_carriers(self):
		carriers_str = ''
		for ele in self.carriers:
			carriers_str += ' '.join(ele.values()) + ' '	
		return carriers_str.strip()

	def str_items(self, items):
		items_str = ''
		for ele in items:
			items_str += ele.__str__() + ' '
		return items_str.strip()

	def str_invoice_num(self):
		invoice_num_str = ''
		for ele in self.invoice_list:
			invoice_num_str += ele.inv_num + ' '
		return invoice_num_str.strip()

	def store_invoice_database(self):
		for invoice in self.invoice_list:
			data = InvoiceTable.objects.create(inv_num=invoice.inv_num,
				card_type=invoice.card_type,
				card_no=invoice.card_no,
				seller_name=invoice.seller_name,
				amount=invoice.amount,
				inv_date=invoice.inv_date.__str__(),
				inv_preiod=invoice.inv_period,
				inv_status=invoice.inv_status,
				inv_donatable=invoice.inv_donatable,
				donate_mark=invoice.donate_mark,
				inv_items=self.str_items(invoice.item))
			data.save()

	def store_carrier_database(self):
		for ele in self.carriers:
			data = CarrierTable.objects.create(
				carrier_type = ele['carrierType'],
				carrier_id = ele['carrierId2'],
				carrier_name = ele['carrierName']
				)
			data.save()

	def store_user_database(self):

		data = UserTable.objects.create(api_key=self.api_key, 
			app_id=self.app_id, 
			card_type=self.card_type, 
			card_no=self.card_no, 
			card_encrypt=self.card_encrypt, 
			carriers_keys=self.str_carriers(), 
			invoice_keys=self.str_invoice_num())
		data.save()

	# def store_seller_database(self):
	# 	for i in self.sellers:
	# 		seller = self.sellers[i]
	# 		data = SellerTable.objects.create(_id = seller._id,
	# 			store_name = seller.store_name,
	# 			branch_name = seller.branch_name,
	# 			address = seller.address,
	# 			longitude = seller.longitude,
	# 			latitude = seller.latitude,
	# 			invoice_keys = str_invoice_num(),
	# 			visit_frequency = seller.visit_frequency,
	# 			consumption = seller.consumption,
	# 			top_item = seller.top_item,
	# 			cluster = seller.cluster)
	# 		data.save()

	def add_seller(self, s, key_name):
		self.sellers[s.id] = Seller(s.id, s.store_name, s.address, s.longitude, s.latitude)
		self.sellers[s.id].set_branch_name(s.branch_name)
		self.sellers[s.id].set_visit_frequency(self.visit_frequency[key_name])
		self.sellers[s.id].set_consumption(self.consumption[key_name])
		if len(self.top_item[key_name]) == 0:
			return
		self.sellers[s.id].set_top_item(self.top_item[key_name][0])
		#self.sellers[s.id]._print()

	def sort_inv_list(self, by_date=True):
		if by_date:
			return sorted(self.invoice_list, key=lambda inv: inv.inv_date.getDate())

	def statistics(self, shop):
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
			#self.sellers.invoice_list.append(invoice)
			self.visit_frequency[invoice.seller_name] += 1
			for item in invoice.item:
				if not is_item(item):
					continue
				if item.description not in self.all_items[invoice.seller_name]:
					self.all_items[invoice.seller_name][item.description] = 0
				self.all_items[invoice.seller_name][item.description] += float(item.quantity)
			self.consumption[invoice.seller_name] += invoice.amount

		for i in self.all_items:
			top = 0  
			for j in self.all_items[i]:
				if top < self.all_items[i][j]:
					top = self.all_items[i][j]
			self.top_item[i] = [] 
			for j in self.all_items[i]:
				if self.all_items[i][j] >= top:
					self.top_item[i].append( (j, self.all_items[i][j]) )

		#for i in self.visit_frequency:
		#	print(i, self.visit_frequency[i], self.consumption[i], self.top_item[i][0].description)
		all_sellers = list_sellers(shop)
		for i in self.visit_frequency:
			seller_on_csv = False
			for j in all_sellers:
				(cur_store_name, cur_branch_name) = split_store_and_branch(i)
				if all_sellers[j].branch_name == cur_branch_name and (cur_store_name=='' and test_store_name(all_sellers[j].store_name) or cur_store_name[:2]==all_sellers[j].store_name[:2]):
					#print(sellers[j].store_name, sellers[j].branch_name, sellers[j].address)
				#if i == sellers[j].branch_name:
					self.add_seller(all_sellers[j],i)
					self.sellers[all_sellers[j].id].invoice_list = tmp_invoice_list[i]
					#print(i, self.visit_frequency[i], self.consumption[i], self.top_item[i][0].description, sellers[j].address)
					seller_on_csv = True
			if not seller_on_csv:
				self.seller_not_on_csv.append(i)


def clustering(user):
	import numpy as np
	from sklearn.cluster import MeanShift, estimate_bandwidth
	from sklearn.datasets.samples_generator import make_blobs
	#print(user)
	X = []
	numbers = []
	'''for number in user:
		X.append([user.longitude, user.latitde])
		numbers.append(number)'''

	for key, value in user.items():
		X.append([float(value.longitude),float(value.latitude)])
		numbers.append(key)
	# Compute clustering with MeanShift
	#print(X)
	#print(numbers)
	#return X,numbers
	ms = MeanShift()
	ms.fit(X)
	labels = ms.labels_
	# fill in the predict labels
	for i in range(len(labels)):
		user[ numbers[i] ].cluster = labels[i]

	cluster_centers = ms.cluster_centers_

	labels_unique = np.unique(labels)
	n_clusters_ = len(labels_unique)

	#print("Number of Clusters : %d" % n_clusters_)

	return user, sorted(user, key=lambda x:user[x].cluster)

def login(account, password):
	api_key = "QWQ4dU9WMzRXa2xoYUdsZA=="
	app_id = "EINV0201505042102"
	card_type = "3J0002"
	card_no = account
	card_encrypt = password
	user = User(api_key, app_id, card_type, card_no, card_encrypt)
	csv = os.path.join(os.path.dirname(os.path.dirname(__file__)),'static','Taipei_shops_with_einvoice.csv')
	#all_sellers1 = list_sellers(csv)
	user.statistics(csv)
	(x, y) = clustering(user.sellers)
	return x,y,user.sort_inv_list()

if __name__ == '__main__':
	TEST = True
	api_key = "QWQ4dU9WMzRXa2xoYUdsZA=="
	app_id = "EINV0201505042102"
	card_type = "3J0002"
	card_no = '/SMV1EFQ'
	card_encrypt = '1212'
	user = User(api_key, app_id, card_type, card_no, card_encrypt)
	csv = os.path.join('..','static','Taipei_shops_with_einvoice.csv')
	#csv = os.path.join(os.path.dirname(os.path.dirname(__file__)),'static','Taipei_shops_with_einvoice.csv')
	#print('csv',csv)
	all_sellers1 = list_sellers(csv)	
	#all_sellers1 = list_sellers("Taipei_shops_with_einvoice.csv")	

	# for inv in user.invoice_list:
	# 	inv._print()
	# print(user.api_key,user.invoice_list)

	user.statistics(csv)
	# for i in user.seller_not_on_csv:
	# 	print(i)
	# print()
	# for i in user.sellers:
	# 	user.sellers[i]._print()
	# for key in user.top_item:
	# 	print(key)
	# 	for item in user.top_item[key]:
	# 		print(item)
	# 	print()
	# for inv in user.sort_inv_list(user.invoice_list):
	# 	inv._print()

	# (x, y) = clustering(user.sellers)

	#for i in x:
	#	x[i]._print()
	# seller_list = []
	# for key in y:
	# 	invoice_list = []
	# 	for invoice in x[key].invoice_list:
	# 		items = []
	# 		for item in invoice.item:
	# 			items.append([item.number,item.description,item.quantity,item.unitPrice,item.amount])
	# 			invoice_list.append([invoice.inv_date.getDate(),invoice.inv_num,invoice.amount, items])
	# 	seller_list.append([key, x[key].longitude, x[key].latitude, x[key].store_name, x[key].branch_name, x[key].address,
	# 	x[key].visit_frequency, x[key].consumption, x[key].top_item, x[key].cluster, invoice_list])
	# print(seller_list)
	#for i in y:
		#x[i]._print()
