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
	try:
		(x,y) = login(account, password)
		tmp = []
		for key, value in y.items():
			tmp.append([key,value.longitude,value.latitude])
			#X.append([value.longitude,value.latitude])
			#numbers.append(value.id)
	except:
		string = traceback.format_exc()
		return render(request,
		'hello_world.html',
		{'test': string},
		context_instance = RequestContext(request)
		)
	return render(request,
		'hello_world.html',
		{'test': tmp},
		context_instance = RequestContext(request)
		)
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
