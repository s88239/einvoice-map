try:
	from py_lib.seller import *
except:
	from seller import *

class Invoice(object):
	def __init__(self, details):
		self.inv_num = details["invNum"]
		self.card_type = details["cardType"]
		self.card_no = details["cardNo"]
		self.seller_name = details["sellerName"]
		self.amount = details["amount"]
		self.inv_date = InvDate(details["invDate"])
		self.inv_period = details["invPeriod"]
		self.inv_status = details["invStatus"]
		self.inv_donatable = details["invDonatable"]
		self.donate_mark = details["donateMark"]
		self.carrier_name = ''
		self.item = []
		self.seller = None

	def add_item(self, _item):
		self.item.append(Item(_item))

	def add_carrier_name(self, user):
		if user.card_no == self.card_no:
			self.carrier_name = '手機條碼'
			return
		for ele in user.carriers:
			if ele['carrierId2'] == self.card_no:
				self.carrier_name = ele['carrierName']
				return
		self.carrier_name = 'Cannot find carrier name'
	
	def add_seller(self, seller):
		self.seller = seller


class InvDate(object):
	def __init__(self, inv_date):
		self.year = inv_date["year"]
		self.month = inv_date["month"]
		self.day = inv_date["date"]
		# self.week_day = inv_date["day"]
		# self.hours = inv_date["hours"]
		# self.minutes = inv_date["minutes"]
		# self.seconds = inv_date["seconds"]
		# self.time = inv_date["time"]
		# self.timezoneOffset = inv_date["timezoneOffset"]
	
	def getDate(self):
		return "{0}/{1:0=2d}/{2:0=2d}".format(int(self.year), int(self.month), int(self.day))
		
	def __str__(self):
		return "{0}/{1:0=2d}/{2:0=2d}".format(int(self.year), int(self.month), int(self.day))

class Item(object):
	def __init__(self, item):
		self.number = item["rowNum"]
		self.description = item["description"].replace(' ', '')
		self.quantity = round(float(item["quantity"]), 2)
		self.unitPrice = round(float(item["unitPrice"]), 2)
		self.amount = round(float(item["amount"]), 2)

	def __str__(self):
		return '|'.join(map(str, [self.number, self.description, self.quantity, self.unitPrice, self.amount]))

		
