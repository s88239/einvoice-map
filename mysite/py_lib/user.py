import sys
import os

try:
	import py_lib.einvoice as einvoice
	from py_lib.seller import list_sellers
	from py_lib.seller import Seller
	from py_lib.invoice import Invoice
except:
	from invoice import Invoice 
	import pickle
	import einvoice
	from seller import list_sellers
	from seller import Seller

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

	def add_seller(self, s):
		i = s.branch_name
		self.sellers[s.id] = Seller(s.id, s.store_name, s.address, s.longitude, s.latitude)
		self.sellers[s.id].set_branch_name(s.branch_name)
		self.sellers[s.id].set_visit_frequency(self.visit_frequency[i])
		self.sellers[s.id].set_consumption(self.consumption[i])
		self.sellers[s.id].set_top_item(self.top_item[i][0].description)
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
				if i == sellers[j].branch_name:
					self.add_seller(sellers[j])
					self.sellers[sellers[j].id].invoice_list = tmp_invoice_list[invoice.seller_name]
					#s = sellers[j]
					#self.sellers[s.id] = Seller(s.id, s.store_name, s.branch_name, s.address, s.longitude, s.latitude)
					#print(i, self.visit_frequency[i], self.consumption[i], self.top_item[i][0].description, sellers[j].address)

def clustering(user):
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

	cluster_centers = ms.cluster_centers_

	labels_unique = np.unique(labels)
	n_clusters_ = len(labels_unique)

	#print("Number of Clusters : %d" % n_clusters_)

	return user, sorted(user, key=lambda x:user[x].cluster)
	#return X,numbers

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
	#(x, y) = clustering(user.sellers)
	#return all_sellers1
	return user

if __name__ == '__main__':
	TEST = True
	api_key = "QWQ4dU9WMzRXa2xoYUdsZA=="
	app_id = "EINV0201505042102"
	card_type = "3J0002"
	card_no = '/SMV1EFQ'
	card_encrypt = '1212'
	user = User(api_key, app_id, card_type, card_no, card_encrypt)
	all_sellers1 = list_sellers("Taipei_shops_with_einvoice.csv")	
	#all_sellers1 = list_sellers("Taipei_shops_with_einvoice.csv")	

	#for inv in user.invoice_list:
	#	inv._print()

	user.statistics('../Taipei_shops_with_einvoice.csv')