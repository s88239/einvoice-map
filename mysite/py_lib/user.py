import sys
import os

try:
	import py_lib.einvoice as einvoice
	from py_lib.seller import list_sellers
	from py_lib.seller import Seller
	from py_lib.invoice import Invoice
	from py_lib.seller import split_store_and_branch
	from py_lib.seller import test_store_name
except:
	from invoice import Invoice 
	import pickle
	import einvoice
	from seller import list_sellers
	from seller import Seller
	from seller import split_store_and_branch
	from seller import test_store_name

'''if sys.version_info >= (2, 7, 9):
	import ssl
	ssl._create_default_https_context = ssl._create_unverified_context'''

class User(object):
	def __init__(self, api_key, app_id, card_type, card_no, card_encrypt):
		self.api_key = api_key
		self.app_id = app_id
		self.card_type = card_type
		self.card_no = card_no
		self.card_encrypt = card_encrypt
		#if not TEST:
		self.invoice_list = einvoice.get_einvoice(api_key, app_id, card_type, card_no, card_encrypt)
		#else:
		#	with open('invoice_list_tmp.pkl', 'rb') as f:
		#		self.invoice_list = pickle.load(f)


		#key is the id of seller
		self.sellers = {}
		#key is the seller_name in invoice
		self.visit_frequency = {}
		self.top_item = {}
		self.items = {}
		self.consumption = {}

	def add_seller(self, s, key_name):
		self.sellers[s.id] = Seller(s.id, s.store_name, s.address, s.longitude, s.latitude)
		self.sellers[s.id].set_branch_name(s.branch_name)
		self.sellers[s.id].set_visit_frequency(self.visit_frequency[key_name])
		self.sellers[s.id].set_consumption(self.consumption[key_name])
		self.sellers[s.id].set_top_item(self.top_item[key_name][0].description)
		#self.sellers[s.id]._print()

	def statistics(self, shop):
		tmp_invoice_list = {}
		for invoice in self.invoice_list:
			if invoice.seller_name not in self.visit_frequency:
				self.visit_frequency[invoice.seller_name] = 0
				self.items[invoice.seller_name] = {}
				self.consumption[invoice.seller_name] = 0.0
			if invoice.seller_name not in tmp_invoice_list:
				tmp_invoice_list[invoice.seller_name] = []
			tmp_invoice_list[invoice.seller_name].append(invoice)
			#self.sellers.invoice_list.append(invoice)
			self.visit_frequency[invoice.seller_name] += 1
			for item in invoice.item:
				if item not in self.items[invoice.seller_name]:
					self.items[invoice.seller_name][item] = 0
				self.items[invoice.seller_name][item] += 1
			self.consumption[invoice.seller_name] += invoice.amount

		for i in self.items:
			top = 0  
			for j in self.items[i]:
				if top < self.items[i][j]:
					top = self.items[i][j]
			self.top_item[i] = [] 
			for j in self.items[i]:
				if self.items[i][j] >= top:
					self.top_item[i].append(j)

		#for i in self.visit_frequency:
		#	print(i, self.visit_frequency[i], self.consumption[i], self.top_item[i][0].description)
		sellers = list_sellers(shop)
		for i in self.visit_frequency:
			for j in sellers:
				(cur_store_name, cur_branch_name) = split_store_and_branch(i)
				if sellers[j].branch_name == cur_branch_name and (cur_store_name=='' and test_store_name(sellers[j].store_name) or cur_store_name[:2]==sellers[j].store_name[:2]):
					print(sellers[j].store_name, sellers[j].branch_name, sellers[j].address)
				#if i == sellers[j].branch_name:
					self.add_seller(sellers[j],i)
					self.sellers[sellers[j].id].invoice_list = tmp_invoice_list[i]
					#print(i, self.visit_frequency[i], self.consumption[i], self.top_item[i][0].description, sellers[j].address)

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
	#TEST
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
	return x,y

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

	#for inv in user.invoice_list:
	#	inv._print()
	#print(user.api_key,user.invoice_list)
	user.statistics(csv)
	(x, y) = clustering(user.sellers)
	#for i in x:
	#	x[i]._print()
	seller_list = []
	for key in y:
		invoice_list = []
		for invoice in x[key].invoice_list:
			items = []
			for item in invoice.item:
				items.append([item.number,item.description,item.quantity,item.unitPrice,item.amount])
				invoice_list.append([invoice.inv_date.getDate(),invoice.inv_num,invoice.amount, items])
		seller_list.append([key, x[key].longitude, x[key].latitude, x[key].store_name, x[key].branch_name, x[key].address,
		x[key].visit_frequency, x[key].consumption, x[key].top_item, x[key].cluster, invoice_list])
	print(seller_list)
	#for i in y:
		#x[i]._print()
