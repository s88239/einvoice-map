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
	y = login(account, password)
	
	return render(request,
		'hello_world.html',
		{'test': y},
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
