
from py_lib import einvoice
from py_lib.invoice import Invoice


class User(object):
	def __init__(self, api_key, app_id, card_type, card_no, card_encrypt):
		self.api_key = api_key
		self.app_id = app_id
		self.card_type = card_type
		self.card_no = card_no
		self.card_encrypt = card_encrypt
		self.invoice_list = einvoice.get_einvoice(api_key, app_id, card_type, card_no, card_encrypt)

		#key is the ID of store
		self.visit_freqency = {}
		self.top_item = {}
		self.consumption = {}

#if __name__ == '__main__':

def clustering(user):
	import numpy as np
	from sklearn.cluster import MeanShift, estimate_bandwidth
	from sklearn.datasets.samples_generator import make_blobs

	X = []
	numbers = []
	for number in user:
		X.append([user.longitude, user.latitde])
		numbers.append(number)

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

	print("Number of Clusters : %d" % n_clusters_)

	return user, sorted(user, key=lambda x:user[x].cluster)
def login(account, password):
	#TEST
	api_key = "QWQ4dU9WMzRXa2xoYUdsZA=="
	app_id = "EINV0201505042102"
	card_type = "3J0002"
	card_no = account
	card_encrypt = password
	user = User(api_key, app_id, card_type, card_no, card_encrypt)
	(x, y) = clustering(user)
	return x, y
	#for inv in user.invoice_list:
	#	inv._print()
	#	print()