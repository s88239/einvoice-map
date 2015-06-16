from seller import list_sellers
from seller import Seller

csv = '../static/Taipei_shops_with_einvoice.csv'
all_sellers1 = list_sellers(csv)
test = ['民安加油站企業有限公司民安海佃加油站','全聯實業(股)公司民生西店分公司','家福(股)公司台南仁德分公司','全聯實業(股)公司華山分公司','千越加油站實業(股)公司西門分公司','中航','齊東分公司']

handled = []
no_company_name_list = ['統一','全家','萊爾富']
def test_store_name(com_name):
	for store_name in no_company_name_list:
		if com_name[:len(store_name)] == store_name:
			return True
	return False

for shop_name in test:
	find_1 = shop_name.find('公司')
	if find_1 != -1 and shop_name[find_1-1]!='分':
		company_name = shop_name[:find_1+2]
		branch_name = shop_name[find_1+2:]
	else:
		company_name = ''
		branch_name = shop_name
	find_2 = company_name.find('')
	#print(shop_name, find_1, company_name, branch_name)
	handled.append([company_name,branch_name])

#for shop_info in handled:
	#print(shop_info[0],shop_info[1])
for key in all_sellers1.keys():
	for shop_pair in handled:
		#print(shop_pair)
		if all_sellers1[key].branch_name == shop_pair[1]:
			if shop_pair[0]=='' and test_store_name(all_sellers1[key].store_name) or shop_pair[0][:2]==all_sellers1[key].store_name[:2]:
				print(all_sellers1[key].store_name, all_sellers1[key].branch_name, all_sellers1[key].address)
