import traceback
from django.shortcuts import render
from django.template import RequestContext
from django.core.context_processors import csrf
from py_lib.user import login

# Create your views here.
from datetime import datetime
from django.http import HttpResponse
test = ["OH~","suck","your","dick"]

def index(request):
	return render(request,'index.html')
def TGOS(request):
	account = request.POST['account']
	password = request.POST['password']
	#try:
	(x,y,einvoice_list) = login(account, password)
	
	# get invoice list by shop
	seller_list = []
	for key in y:
		invoice_list = []
		for invoice in x[key].invoice_list:
			items = []
			for item in invoice.item:
				items.append([item.number,item.description,item.quantity,item.unitPrice,item.amount])
			invoice_list.append([invoice.inv_date.getDate(),invoice.inv_num,invoice.amount, items])

		if len(x[key].top_item) != 0:
			top_item_str = x[key].top_item[0] + ' x ' + str(x[key].top_item[1])
		else:
			top_item_str = 'none'

		seller_list.append([key,
		x[key].longitude,
		x[key].latitude,
		x[key].store_name,
		x[key].branch_name,
		x[key].address,
		x[key].visit_frequency,
		x[key].consumption,
		top_item_str,
		x[key].cluster,
		invoice_list])

	# get sorted invoice list
	sorted_invoice_list = []
	for cur_einvoice in einvoice_list:
		items = []
		for item in cur_einvoice.item:
			items.append([item.number,item.description,item.quantity,item.unitPrice,item.amount])
		sorted_invoice_list.append([
			cur_einvoice.inv_num,
			cur_einvoice.card_type,
			cur_einvoice.card_no,
			cur_einvoice.seller_name,
			cur_einvoice.amount,
			cur_einvoice.inv_date.getDate(),
			cur_einvoice.inv_period,
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
		{'sellers': seller_list, 'einvoice': sorted_invoice_list},
		context_instance = RequestContext(request)
		)
#{'current_time': datetime.now()}
def hello_world(request):
	return render(request,'output.html',
	{'test': test},
	context_instance = RequestContext(request))
def demo(request):
	return render(request,'demo.html')
