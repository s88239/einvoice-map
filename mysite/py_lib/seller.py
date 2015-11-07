# -*- coding: utf-8 -*-
import csv

class Seller(object):
	def __init__(self, _id, store_name, address, longitude, latitude):
		store_name = replace_seller_name(store_name.strip())
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

	def __str__(self):
		return str(self.id) + ' ' + self.store_name + ' ' + self.branch_name + ' ' + self.address + ' ' + str(self.longitude) + ' ' + str(self.latitude)

def list_sellers(csv_file):
	#key is the ID
	sellers = {}
	with open(csv_file, 'r', errors='ignore') as f:
		for i, row in enumerate(csv.reader(f)):
			row = [s.replace("\n", "") for s in row]
			sellers[i] = Seller(i, row[1], row[2], row[3], row[4])
	return sellers


replace_list = [('臺','台'),('（','('),('）',')'),('0','０'),('○','０'),('1','一'),('１','一'),('2','二'),('２','二'),('3','三'),('３','三'),('4','四'),('４','四'),('5','五'),('５','五'),('6','六'),('６''六'),('7','七'),('７','七'),('8','八'),('８','八'),('9','九'),('９','九'),('台灣糖業','台糖'),('家福','家樂福'),('台灣家樂福','家樂福'),('來來超商','OK超商'),('三商行','美廉社'),('安心食品服務','摩斯漢堡'),('惠康百貨','頂好'),('美味達人','85度C')]
def replace_seller_name(shop_name):
	for replace_item in replace_list:
		shop_name = shop_name.replace(replace_item[0], replace_item[1])
	return shop_name

def split_store_and_branch(shop_name):
	find_dash = shop_name.find('-')
	if find_dash != -1: # find the delimeter -
		company_name = shop_name[:find_dash]
		branch_name = shop_name[find_dash+1:]
		return company_name.strip(), branch_name.strip()

	find_1 = shop_name.find('公司')
	if find_1 != -1 and shop_name[find_1-1]!='分': # find the delimeter 公司
		company_name = shop_name[:find_1+2]
		branch_name = shop_name[find_1+2:]
	else:
		find_2 = shop_name.find('(股)') # find the delimeter (股)
		if find_2 != -1:
			company_name = shop_name[:find_2]
			branch_name = shop_name[find_2+3:]
		else: # can't split
			company_name = ''
			branch_name = shop_name

	return company_name.strip(), branch_name.strip()

no_company_name_list = ['統一','全家','萊爾富','台灣楓康超市','千越自助加油站','太平洋崇光百貨','中華電信','麥當勞','台糖量販','台糖健康超市','台糖蜜鄰超市','台灣菸酒']
def test_store_name(com_name):
	for store_name in no_company_name_list:
		if com_name[:len(store_name)] == store_name:
			return True
	return False

def match_seller(einvoice_seller_name, test_seller):
	full_einvoice_seller_name = replace_seller_name( einvoice_seller_name.strip() );
	(cur_store_name, cur_branch_name) = split_store_and_branch(full_einvoice_seller_name)
	store_name = test_seller.store_name
	branch_name = test_seller.branch_name
	#print(full_einvoice_seller_name,":",cur_store_name, "-", cur_branch_name," / ",store_name,"-",branch_name)
	if full_einvoice_seller_name == store_name:
		return True
	elif einvoice_seller_name == store_name and branch_name == "": # complete matched
		return True
	elif branch_name == cur_branch_name and (cur_store_name == '' and test_store_name(store_name) ): # matched the shop without store name
		return True
	elif store_name in cur_store_name and branch_name == cur_branch_name: # match store name and branch name
		return True

	return False

if __name__ == '__main__':
	#TEST
	#all_sellers1 = list_sellers("Taipei_shops_with_einvoice.csv")
	seller_name_list = ['交通部臺灣鐵路管理局餐旅服務總所臺中鐵路餐廳','全家便利商店-高雄市第三○九分公司','來來超商-第1182分公司','台灣家樂福-北大分公司','美華泰-嘉義中山分公司','台糖-油品事業部嘉保加油站']
	test_seller_list = ['交通部臺灣鐵路管理局餐旅服務總所臺中鐵路餐廳','高雄市第309分公司','來來超商股份有限公司第１１８２分公司','家福-北大分公司','美華泰(股)公司嘉義中山分公司','台灣糖業（股）公司油品事業部嘉保加油站']
	seller_list = []
	for i in range(0,len(seller_name_list)):
		print(i,":",seller_name_list[i])
		seller_list.append(Seller(i,seller_name_list[i],'台南','121','23'))

	for i in range(0,len(seller_name_list)):
		print(i,'@',match_seller(test_seller_list[i],seller_list[i]))