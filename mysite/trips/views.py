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
def hello_world(request):
	account = request.POST['account']
	password = request.POST['password']
<<<<<<< HEAD
	try:
		(x,y) = login(account, password)
		'''tmp = []
=======
	#try:
	user = login(account, password)
	
	return render(request,
		'TGOS.html',
		{'sellers': user},
		context_instance = RequestContext(request)
		)
	'''seller_list = []
	for key in user.sellers.keys():
		invoice_list = []
		for invoice in user.sellers[key].invoice_list:
			items = []
			for item in invoice.item:
				items.append([item.number,item.description,item.quantity,item.unitPrice,item.amount])
			invoice_list.append([invoice.inv_num,invoice.seller_name,invoice.amount, items])
			
		seller_list.append([key,
		user.sellers[key].longitude,
		user.sellers[key].latitude,
		user.sellers[key].store_name,
		user.sellers[key].branch_name,
		user.sellers[key].address,
		user.sellers[key].visit_frequency,
		user.sellers[key].consumption,
		user.sellers[key].top_item,
		user.sellers[key].cluster,
		invoice_list])
		#(x,y) = login(account, password)
		tmp = []
>>>>>>> 01366e9ccad9a1decae64544082ce093886de611
		for key, value in y.items():
			tmp.append([key,value.longitude,value.latitude])'''
			#X.append([value.longitude,value.latitude])
			#numbers.append(value.id)
<<<<<<< HEAD
		return render(request,
			'hello_world.html',
			{'test': x, 'test2':y},
			context_instance = RequestContext(request)
			)
	except:
=======
	'''except:
>>>>>>> 01366e9ccad9a1decae64544082ce093886de611
		string = traceback.format_exc()
		return render(request,
		'hello_world.html',
		{'test': string},
		context_instance = RequestContext(request)
		)
<<<<<<< HEAD
=======
	return render(request,
		'hello_world.html',
		{'test': user},
		context_instance = RequestContext(request)
		)'''
>>>>>>> 01366e9ccad9a1decae64544082ce093886de611
#{'current_time': datetime.now()}
def TGOS(request):
	account = request.POST['account']
	password = request.POST['password']
	x, y = login(account, password)
	
	return render(request,'TGOS.html',
	{'test': y},
	context_instance = RequestContext(request))
def home(request):
	return render(request,'home.html')
