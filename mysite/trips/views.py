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
	(x,y) = login(account, password)
	
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
	'''except:
		string = traceback.format_exc()
		return render(request,
		'hello_world.html',
		{'test': string},
		context_instance = RequestContext(request)
		)'''
	return render(request,
		'TGOS.html',
		{'sellers': seller_list},
		context_instance = RequestContext(request)
		)
#{'current_time': datetime.now()}
def hello_world(request):
	return render(request,'output.html',
	{'test': test},
	context_instance = RequestContext(request))
def demo(request):
	return render(request,'demo.html')
