from django.http import *
#from django.core.context_processors import csrf
from django import shortcuts
import utils
from django.views.decorators.csrf import csrf_exempt
#import time


def index(request):
	if request.user.is_anonymous() or not request.user.is_user:
		return shortcuts.redirect('/horizon/auth/login/')

	instances = utils.get_instances(request)
	user = utils.get_user(request)
	projects = utils.get_projects(request,user)

	for instance in instances:
		instance['console_url'] = utils.get_console_url(request,instance)

	limit = utils.get_project_limit(request)

	return shortcuts.render_to_response('index.html',{"user":user,"instances":instances,"projects":projects,"tenant_name":request.user.tenant_name,'limit':limit})


def log(request,instance_id):
	if request.user.is_anonymous() or not request.user.is_user:
		return shortcuts.redirect('/horizon/auth/login/')

	instances = utils.get_instances(request,overview=True)
	user = utils.get_user(request)
	projects = utils.get_projects(request,user)
	for instance in instances:
		if getattr(instance,'id','') == instance_id:
			ins = instance

	try:
		console_log = utils.get_log_data(request,instance_id)
	except Exception:
		console_log = "Unable to get log data!"

	console_url = utils.get_console_url(request,ins)
	
	return shortcuts.render_to_response('log.html',{"user":user,"instances":instances,"projects":projects,"tenant_name":request.user.tenant_name,"current_instance":ins,"console_log":console_log})


def full_log(request,instance_id):
	data = utils.get_log_data(request,instance_id,length=None)
	response = http.HttpResponse(mimetype='text/plain')
	response.write(data)
	response.flush()
	return response

@csrf_exempt
def update(request):
	info = {}
	data = request.POST
	if data['password'] == '':
		info['email'] = data['email']
		info['password'] = None
	else:
		info['email'] = data['email']
		info['password'] = data['password']

	utils.update_userinfo(request,info)

	if data['password'] == '':
		return shortcuts.redirect('/horizon/userdash')
	else:
		return shortcuts.redirect('/horizon/auth/login')







