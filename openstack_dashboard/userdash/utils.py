import api
from horizon import exceptions
from django.utils.datastructures import SortedDict  # noqa
from django.utils.translation import ugettext_lazy as _  # noqa
from horizon.templatetags import sizeformat
from django.conf import settings
import json,ast

import logging
logging.basicConfig(filename='/home/zeus/Desktop/mylog')


POWER_STATES = {
    0: "NO STATE",
    1: "RUNNING",
    2: "BLOCKED",
    3: "PAUSED",
    4: "SHUTDOWN",
    5: "SHUTOFF",
    6: "CRASHED",
    7: "SUSPENDED",
    8: "FAILED",
    9: "BUILDING",
}

def get_size(instance):
    if hasattr(instance, "full_flavor"):
        size_string = _("%(name)s | %(RAM)s RAM | %(VCPU)s VCPU "
                        "| %(disk)s Disk")
        vals = {'name': instance.full_flavor.name,
                'RAM': sizeformat.mbformat(instance.full_flavor.ram),
                'VCPU': instance.full_flavor.vcpus,
                'disk': sizeformat.diskgbformat(instance.full_flavor.disk)}
        return size_string % vals
    return "No Available"

def get_cpu_statistics(request,instance_id,period):
	raw_data = api.ceilometer.statistic_list(request,'cpu',query=[{'field':'resource_id','op':'eq','value':instance_id}],period=period)

	length = len(raw_data)

	if period==3600:
		if length >24:
			raw_data = raw_data[-24:]
	if period == 28800:
		if length > 21:
			raw_data = raw_data[-21:]
	if period == 86400:
		if length > 30:
			raw_data == raw_data[-30:]

	statistics = []
	for data in raw_data:
		statistic = {}
		statistic['count'] = getattr(data,'count')
		statistic['max'] = round(getattr(data,'max') / 10**12,2)
		statistic['min'] = round(getattr(data,'min') / 10**12,2)
		statistic['sum'] = round(getattr(data,'sum') / 10**12,2)
		statistic['avg'] = round(getattr(data,'avg') / 10**12,2)
		statistic['period'] = getattr(data,'period')
		statistic['period_start'] = getattr(data,'period_start').replace("T"," ")
		statistic['period_end'] = getattr(data,'period_end').replace("T"," ")
		statistic['duration'] = getattr(data,'duration')
		statistic['duration_start'] = getattr(data,'duration_start').replace("T"," ")
		statistic['duration_end'] = getattr(data,'duration_end').replace("T"," ")
		statistics.append(statistic)
	
	return {"cpu":statistics}

def get_network_statistics(request,instance_id,period):
	resources = api.ceilometer.resource_list(request)
	for resource in resources:
		metadata = getattr(resource,'metadata')
		metadata = ast.literal_eval(json.dumps(metadata))
		if metadata.has_key('instance_id'):
			if metadata['instance_id'] == instance_id:
				network_id = metadata['fref']

	raw_data_outgoing = api.ceilometer.statistic_list(request,'network.outgoing.bytes',query=[{'field':'resource_id','op':'eq','value':network_id}],period=period)
	raw_data_incoming = api.ceilometer.statistic_list(request,'network.incoming.bytes',query=[{'field':'resource_id','op':'eq','value':network_id}],period=period)
	
	length = len(raw_data_incoming)
	if period==3600:
		if length >24:
			raw_data_incoming = raw_data_incoming[-24:]
	if period == 28800:
		if length > 21:
			raw_data_incoming = raw_data_incoming[-21:]
	if period == 86400:
		if length > 30:
			raw_data_incoming == raw_data_incoming[-30:]

	length = len(raw_data_outgoing)
	if period==3600:
		if length >24:
			raw_data_outgoing = raw_data_outgoing[-24:]
	if period == 28800:
		if length > 21:
			raw_data_outgoing = raw_data_outgoing[-21:]
	if period == 86400:
		if length > 30:
			raw_data_outgoing == raw_data_outgoing[-30:]

	statistics_incoming = []
	for data in raw_data_incoming:
		statistic = {}
		statistic['count'] = getattr(data,'count')
		statistic['max'] = round(getattr(data,'max') / 1024,2)
		statistic['min'] = round(getattr(data,'min') / 1024,2)
		statistic['sum'] = round(getattr(data,'sum') / 1024,2)
		statistic['avg'] = round(getattr(data,'avg') / 1024,2)
		statistic['period'] = getattr(data,'period')
		statistic['period_start'] = getattr(data,'period_start').replace("T"," ")
		statistic['period_end'] = getattr(data,'period_end').replace("T"," ")
		statistic['duration'] = getattr(data,'duration')
		statistic['duration_start'] = getattr(data,'duration_start').replace("T"," ")
		statistic['duration_end'] = getattr(data,'duration_end').replace("T"," ")
		statistics_incoming.append(statistic)

	statistics_outgoing = []
	for data in raw_data_outgoing:
		statistic = {}
		statistic['count'] = getattr(data,'count')
		statistic['max'] = round(getattr(data,'max') / 1024,2)
		statistic['min'] = round(getattr(data,'min') / 1024,2)
		statistic['sum'] = round(getattr(data,'sum') / 1024,2)
		statistic['avg'] = round(getattr(data,'avg') / 1024,2)
		statistic['period'] = getattr(data,'period')
		statistic['period_start'] = getattr(data,'period_start').replace("T"," ")
		statistic['period_end'] = getattr(data,'period_end').replace("T"," ")
		statistic['duration'] = getattr(data,'duration')
		statistic['duration_start'] = getattr(data,'duration_start').replace("T"," ")
		statistic['duration_end'] = getattr(data,'duration_end').replace("T"," ")
		statistics_outgoing.append(statistic)

	return {'network_incoming_bytes':statistics_incoming,'network_outgoing_bytes':statistics_outgoing}

def get_disk_statistics(request,instance_id,period):
	raw_data_read = api.ceilometer.statistic_list(request,'disk.read.bytes',query=[{'field':'resource_id','op':'eq','value':instance_id}],period=period)
	raw_data_write = api.ceilometer.statistic_list(request,'disk.write.bytes',query=[{'field':'resource_id','op':'eq','value':instance_id}],period=period)
	
	length = len(raw_data_read)
	if period==3600:
		if length >24:
			raw_data_read = raw_data_read[-24:]
	if period == 28800:
		if length > 21:
			raw_data_read = raw_data_read[-21:]
	if period == 86400:
		if length > 30:
			raw_data_read == raw_data_read[-30:]

	length = len(raw_data_write)
	if period==3600:
		if length >24:
			raw_data_write = raw_data_write[-24:]
	if period == 28800:
		if length > 21:
			raw_data_write = raw_data_write[-21:]
	if period == 86400:
		if length > 30:
			raw_data_write == raw_data_write[-30:]

	statistics_read = []
	for data in raw_data_read:
		statistic = {}
		statistic['count'] = getattr(data,'count')
		statistic['max'] = round(getattr(data,'max') / 2**20,2)
		statistic['min'] = round(getattr(data,'min') / 2**20,2)
		statistic['sum'] = round(getattr(data,'sum') / 2**20,2)
		statistic['avg'] = round(getattr(data,'avg') / 2**20,2)
		statistic['period'] = getattr(data,'period')
		statistic['period_start'] = getattr(data,'period_start').replace("T"," ")
		statistic['period_end'] = getattr(data,'period_end').replace("T"," ")
		statistic['duration'] = getattr(data,'duration')
		statistic['duration_start'] = getattr(data,'duration_start').replace("T"," ")
		statistic['duration_end'] = getattr(data,'duration_end').replace("T"," ")
		statistics_read.append(statistic)

	statistics_write = []
	for data in raw_data_write:
		statistic = {}
		statistic['count'] = getattr(data,'count')
		statistic['max'] = round(getattr(data,'max') / 2**20,2)
		statistic['min'] = round(getattr(data,'min') / 2**20,2)
		statistic['sum'] = round(getattr(data,'sum') / 2**20,2)
		statistic['avg'] = round(getattr(data,'avg') / 2**20,2)
		statistic['period'] = getattr(data,'period')
		statistic['period_start'] = getattr(data,'period_start').replace("T"," ")
		statistic['period_end'] = getattr(data,'period_end').replace("T"," ")
		statistic['duration'] = getattr(data,'duration')
		statistic['duration_start'] = getattr(data,'duration_start').replace("T"," ")
		statistic['duration_end'] = getattr(data,'duration_end').replace("T"," ")
		statistics_write.append(statistic)

	return {"disk_read_bytes":statistics_read,"disk_write_bytes":statistics_write}

def get_instances(request,instance_id=None,overview=False):
	try:
		instances, _more = api.nova.server_list(request)
	except Exception:
		_more = False
		instances = []
		exceptions.handle(request,_('Unable to retrieve instances.'))

	if instances:
			try:
				flavors = api.nova.flavor_list(request)
			except Exception:
				flavors = []
				exceptions.handle(request, ignore=True)

			try:
				images, more = api.glance.image_list_detailed(request)
			except Exception:
				images = []
				exceptions.handle(request, ignore=True)

			full_flavors = SortedDict([(str(flavor.id), flavor) for flavor in flavors])
			image_map = SortedDict([(str(image.id), image) for image in images])

			# Loop through instances to get flavor info.
			for instance in instances:
				if hasattr(instance, 'image'):
					# Instance from image returns dict
					if isinstance(instance.image, dict):
						if instance.image.get('id') in image_map:
							instance.image = image_map[instance.image['id']]
					else:
						# Instance from volume returns a string
						instance.image = {'name':instance.image if instance.image else _("-")}

				try:
					flavor_id = instance.flavor["id"]
					if flavor_id in full_flavors:
						instance.full_flavor = full_flavors[flavor_id]
					else:
						instance.full_flavor = api.nova.flavor_get(
							self.request, flavor_id)
				except Exception:
					msg = _('Unable to retrieve instance size information.')
					exceptions.handle(self.request, msg)

	if overview == False:
		filteredinstances = []
		if instance_id == None:
			for instance in instances:
				ins = {}
				ins['name'] = getattr(instance,'name','')
				ins['image'] = getattr(instance,'image_name','')
				ins['status'] = getattr(instance,'status','')
				ins['powerstate'] = POWER_STATES.get(getattr(instance, "OS-EXT-STS:power_state", 0), '')
				ins['flavor'] = get_size(instance)
				ins['id'] = getattr(instance,'id','')
				addresses = getattr(instance,'addresses')
				vmnet = addresses['vmnet']
				ip = vmnet[0]['addr']
				ins['ip'] = ip
				ins['keyname'] = getattr(instance,'key_name')
				ins['created'] = getattr(instance,'created')
				filteredinstances.append(ins)
		else:
			for instance in instances:
				if getattr(instance,'id','') == instance_id:
					ins = {}
					ins['name'] = getattr(instance,'name','')
					ins['image'] = getattr(instance,'image_name','')
					ins['status'] = getattr(instance,'status','')
					ins['powerstate'] = POWER_STATES.get(getattr(instance, "OS-EXT-STS:power_state", 0), '')
					ins['flavor'] = get_size(instance)
					ins['id'] = getattr(instance,'id','')
					addresses = getattr(instance,'addresses')
					vmnet = addresses['vmnet']
					ip = vmnet[0]['addr']
					ins['ip'] = ip
					ins['keyname'] = getattr(instance,'key_name')
					ins['created'] = getattr(instance,'created')
					return ins;

		return filteredinstances
	else:
		if instance_id == None:
			return instances
		else:
			for instance in instances:
				if getattr(instance,'id','') == instance_id:
					return  instance

def get_user(request):
	try:
		users = api.keystone.user_list(request,admin = False)
	except Exception:
		exceptions.handle(request,_("Unable to get users"))
		
	for user in users:
		if user.name == request.user.username:
			return user

def get_projects(request,user):
	try:
		projects = api.keystone.tenant_list(request,user=user)[0]
	except Exception:
		exceptions.handle(request,_("Unable to get projects"))

	return projects

def get_project_limit(request):
	usage = api.nova.tenant_absolute_limits(request)
	limit = {}
	limit['instanceUsed'] = usage['totalInstancesUsed']
	limit['instanceUnused'] = usage['maxTotalInstances']-usage['totalInstancesUsed']
	limit['ramUsed'] = usage['totalRAMUsed'] / 1024
	limit['ramUnused'] = (usage['maxTotalRAMSize'] - usage['totalRAMUsed']) / 1024
	limit['coreUsed'] = usage['totalCoresUsed']
	limit['coreUnused'] = usage['maxTotalCores'] - usage['totalCoresUsed']
	return limit

def start_instance(request,instance_id):
	api.nova.server_start(request, instance_id)

def stop_instance(request,instance_id):
	api.nova.server_stop(request, instance_id)

def suspend_instance(request,instance_id):
	api.nova.server_suspend(request, instance_id)

def resume_instance(request,instance_id):
	api.nova.server_resume(request, instance_id)

def update_userinfo(request,data):
	if data.has_key('password'):
		api.keystone.user_update_own_password(request,None,data['password'],email=data['email'])
	else:
		api.keystone.user_update(request,request.user,**data)

def get_log_data(request,instance_id,length=40):
	data = api.nova.server_console_output(request,instance_id,tail_length=length)
	return  data;

def get_console_url(request,instance):
	console_type = getattr(settings, 'CONSOLE_TYPE', 'AUTO')
	if console_type == 'AUTO':
		try:
			console = api.nova.server_vnc_console(request, instance['id'])
			console_url = "%s&title=%s(%s)" % (console.url,getattr(instance, "name", ""),instance['id'])
		except Exception:
			try:
				console = api.nova.server_spice_console(request,instance['id'])
				console_url = "%s&title=%s(%s)" % (console.url,getattr(instance, "name", ""),instance['id'])
			except Exception:
				console_url = None
	elif console_type == 'VNC':
		try:
			console = api.nova.server_vnc_console(request, instance['id'])
			console_url = "%s&title=%s(%s)" % (console.url,getattr(instance, "name", ""),instance['id'])
		except Exception:
			console_url = None
	elif console_type == 'SPICE':
		try:
			console = api.nova.server_spice_console(request, instance.id)
			console_url = "%s&title=%s(%s)" % (console.url,getattr(instance, "name", ""),instance['id'])
		except Exception:
			console_url = None
	else:
		console_url = None

	return console_url

