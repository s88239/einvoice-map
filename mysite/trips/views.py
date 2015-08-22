import traceback
from django.shortcuts import render
from django.template import RequestContext
from django.core.context_processors import csrf
from py_lib.user import login

# Create your views here.
from datetime import datetime
from django.http import HttpResponse

def index(request):
	return render(request,'index.html')
def TGOS(request):
	account = request.POST['account']
	password = request.POST['password']
	#try:
	(sellers,sorted_key,einvoice_list,center) = login(account, password)
	
	# get center point
	center_point = [center[0], center[1]];
	# get invoice list by shop
	seller_list = []
	for key in sorted_key:
		invoice_list = []
		for invoice in sellers[key].invoice_list:
			items = []
			for item in invoice.item:
				items.append([item.description,item.quantity,item.unitPrice,item.amount])
			invoice_list.append([invoice.inv_date.getDate(),invoice.inv_num,invoice.amount, items])

		if len(sellers[key].top_item) != 0:
			top_item_str = sellers[key].top_item[0] + ' x ' + str( round(sellers[key].top_item[1], 2) )
		else:
			top_item_str = 'none'

		seller_list.append([key,
		sellers[key].longitude,
		sellers[key].latitude,
		sellers[key].store_name,
		sellers[key].branch_name,
		sellers[key].address,
		sellers[key].visit_frequency,
		sellers[key].consumption,
		top_item_str,
		sellers[key].cluster,
		invoice_list])

	# get sorted invoice list
	sorted_invoice_list = []
	for cur_einvoice in einvoice_list:
		items = []
		for item in cur_einvoice.item:
			items.append([item.description,item.quantity,item.unitPrice,item.amount])

		cur_seller_idx = -1
		for seller_idx in range(len(seller_list)): # get the idx of seller in einvoice
			if cur_einvoice.seller.store_name == seller_list[seller_idx].store_name and cur_einvoice.seller.branch_name == seller_list[seller_idx].branch_name:
				cur_seller_idx = seller_idx
				break
		sorted_invoice_list.append([
			cur_einvoice.inv_date.getDate(),
			cur_einvoice.carrier_name,
			cur_einvoice.card_no,
			cur_einvoice.seller_name,
			cur_einvoice.amount,
			cur_einvoice.inv_num,
			cur_seller_idx,
			items])
	'''except:
		string = traceback.format_exc()
		return render(request,
		'hello_world.html',
		{'test': string},
		context_instance = RequestContext(request)
		)'''
	return render(request,
		'TGOS.html',
		{'sellers': seller_list, 'einvoice': sorted_invoice_list, 'center': center_point},
		context_instance = RequestContext(request)
		)
#{'current_time': datetime.now()}
def hello_world(request):
	return render(request,'output.html',
	{'test': test},
	context_instance = RequestContext(request))
def demo(request):
	return render(request,'demo.html')
