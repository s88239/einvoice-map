from django.db import models

# Create your models here.
class UserTable(models.Model):
	api_key = models.CharField(max_length=100)
	app_id = models.CharField(max_length=100)
	card_type = models.CharField(max_length=100)
	card_no = models.CharField(max_length=100, primary_key=True)
	card_encrypt = models.CharField(max_length=100)
	carriers_keys = models.CharField(max_length=1000)

	invoice_keys = models.TextField(max_length=100000)
	# seller_keys = models.CharField(max_length=100)

	def __str__(self):
		return self.card_no

class CarrierTable(models.Model):
	carrier_type = models.CharField(max_length=100)
	carrier_id = models.CharField(max_length=100, primary_key=True)
	carrier_name = models.CharField(max_length=100)

	def __str__(self):
		return self.carrier_id

class InvoiceTable(models.Model):
	card_type = models.CharField(max_length=100)
	inv_num = models.CharField(max_length=100, primary_key=True)
	card_no = models.CharField(max_length=100)
	carrier_name = models.CharField(max_length=100, null=True)
	seller_name = models.CharField(max_length=100)
	amount = models.CharField(max_length=100)
	inv_date = models.CharField(max_length=100)
	inv_preiod = models.CharField(max_length=100)
	inv_status = models.CharField(max_length=100)
	inv_donatable = models.CharField(max_length=100)
	donate_mark = models.CharField(max_length=100)
	inv_items = models.CharField(max_length=1000)

	def __str__(self):
		return self.inv_num


class UnMatchSellerTable(models.Model):
	seller_name = models.CharField(max_length=100, primary_key=True)
	
	def __str__(self):
		return self.seller_name
