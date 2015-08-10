import csv

class Seller(object):
	def __init__(self, _id, store_name, address, longitude, latitude):
		self.id = _id
		self.store_name = store_name if store_name.find("-") == -1 else store_name[:store_name.find("-")]
		self.branch_name = "" if store_name.find("-") == -1 else store_name[store_name.find("-")+1:]
		self.address = address
		self.longitude = longitude
		self.latitude = latitude

		#for user
		self.invoice_list = []
		self.visit_frequency = 0
		self.consumption = 0.0
		self.top_item = ''
		self.cluster = 0

	def set_branch_name(self, n):
		self.branch_name = n

	def set_visit_frequency(self, f):
		self.visit_frequency = f

	def set_consumption(self, c):
		self.consumption = c
		
	def set_top_item(self, i):
		self.top_item = i

	def _print(self):
		print(self.id, self.store_name, self.branch_name, self.address, self.longitude, self.latitude, self.visit_frequency, self.consumption, self.top_item, self.cluster)

def list_sellers(csv_file):
	#key is the ID
	sellers = {}
	with open(csv_file, 'r', errors='ignore') as f:
		for i, row in enumerate(csv.reader(f)):
			row = [s.replace("\n", "") for s in row]
			sellers[i] = Seller(i, row[1], row[2], row[3], row[4])
	return sellers

def split_store_and_branch(shop_name):
	find_1 = shop_name.find('公司')
	if find_1 != -1 and shop_name[find_1-1]!='分':
		company_name = shop_name[:find_1+2]
		branch_name = shop_name[find_1+2:]
	else:
		company_name = ''
		branch_name = shop_name
	return company_name, branch_name

no_company_name_list = ['統一','全家','萊爾富','台灣楓康超市','千越自助加油站']
def test_store_name(com_name):
	for store_name in no_company_name_list:
		if com_name[:len(store_name)] == store_name:
			return True
	return False

if __name__ == '__main__':
	#TEST
	all_sellers1 = list_sellers("Taipei_shops_with_einvoice.csv")
	#all_sellers2 = list_sellers("Taipei_shops_with_einvoice.csv")
	#for key in sellers:
	for i in range(1, 2000):
		sellers[i]._print()
