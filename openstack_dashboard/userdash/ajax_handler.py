from django.http import *
from django import shortcuts
import utils
from django.utils import simplejson
import time

def start_instance(request,instance_id):
	try:
		utils.start_instance(request, instance_id)
	except Exception,e:
		return HttpResponse(simplejson.dumps({"status":"error","message":e},ensure_ascii=False))
		
	instance = utils.get_instances(request,instance_id)
	while instance['status'] != 'ACTIVE':
		time.sleep(3)
		instance = utils.get_instances(request,instance_id)

	message = "Instance "+instance_id+" started successfully."
	return HttpResponse(simplejson.dumps({"status":"success","message":message},ensure_ascii=False))

def stop_instance(request,instance_id):
	try:
		utils.stop_instance(request, instance_id)
	except Exception,e:
		return HttpResponse(simplejson.dumps({"status":"error","message":e},ensure_ascii=False))

	instance = utils.get_instances(request,instance_id)
	while instance['status'] != 'SHUTOFF':
		time.sleep(3)
		instance = utils.get_instances(request,instance_id)
	
	message = "Instance "+instance_id+" stopped successfully."
	return HttpResponse(simplejson.dumps({"status":"success","message":message},ensure_ascii=False))
	

def suspend_instance(request,instance_id):
	try:
		utils.suspend_instance(request,instance_id)
	except Exception,e:
		return HttpResponse(simplejson.dumps({"status":"error","message":e},ensure_ascii=False))

	instance = utils.get_instances(request,instance_id)
	while instance['status'] != 'SUSPENDED':
		time.sleep(3)
		instance = utils.get_instances(request,instance_id)

	message = "Instance "+instance_id+" suspended successfully."
	return HttpResponse(simplejson.dumps({"status":"success","message":message},ensure_ascii=False))

def resume_instance(request,instance_id):
	try:
		utils.resume_instance(request,instance_id)
	except Exception,e:
		return HttpResponse('error:%s' % e)

	instance = utils.get_instances(request,instance_id)
	while instance['status'] != 'ACTIVE':
		time.sleep(3)
		instance = utils.get_instances(request,instance_id)

	message = "Instance "+instance_id+" resumed successfully."
	return HttpResponse(simplejson.dumps({"status":"success","message":message},ensure_ascii=False))

def renew_instance(request,instance_id):
	instance = utils.get_instances(request,instance_id);
	return HttpResponse(simplejson.dumps({"status":instance['status'],"powerstate":instance['powerstate']},ensure_ascii=False))


def get_cpu_statistics(request,instance_id,period):
	statistics = utils.get_cpu_statistics(request,instance_id,period)
	return HttpResponse(simplejson.dumps(statistics,ensure_ascii=False))

def get_network_statistics(request,instance_id,period):
	statistics = utils.get_network_statistics(request,instance_id,period)
	return HttpResponse(simplejson.dumps(statistics,ensure_ascii=False))

def get_disk_statistics(request,instance_id,period):
	statistics = utils.get_disk_statistics(request,instance_id,period)
	return HttpResponse(simplejson.dumps(statistics,ensure_ascii=False))


def latest_log(request,instance_id,length):
	data = utils.get_log_data(request,instance_id,length=length)
	return HttpResponse(data)