from django.conf.urls.defaults import patterns  # noqa
from django.conf.urls.defaults import url  # noqa


urlpatterns = patterns('openstack_dashboard.userdash.views',
    url(r'^$', 'index', name='index'),
    url(r'^(?P<instance_id>[^/]+)/log/$','log',name='log'),
    url(r'^(?P<instance_id>[^/]+)/fulllog/$','full_log',name='full_log'),
    url(r'^update$', 'update', name='update'),
)

urlpatterns += patterns('openstack_dashboard.userdash.ajax_handler',
    url(r'^(?P<instance_id>[^/]+)/startinstance/$','start_instance',name='start_instance'),
    url(r'^(?P<instance_id>[^/]+)/stopinstance/$','stop_instance',name='stop_instance'),
    url(r'^(?P<instance_id>[^/]+)/suspendinstance/$','suspend_instance',name='suspend_instance'),
    url(r'^(?P<instance_id>[^/]+)/resumeinstance/$','resume_instance',name='resume_instance'),
    url(r'^(?P<instance_id>[^/]+)/renewinstance/$','renew_instance',name='renew_instance'),
    url(r'^(?P<instance_id>[^/]+)/getcpustatistics/(?P<period>\d+)/$','get_cpu_statistics',name='get_cpu_statistics'),
    url(r'^(?P<instance_id>[^/]+)/getnetworkstatistics/(?P<period>\d+)/$','get_network_statistics',name='get_network_statistics'),
    url(r'^(?P<instance_id>[^/]+)/getdiskstatistics/(?P<period>\d+)/$','get_disk_statistics',name='get_disk_statistics'),
    url(r'^(?P<instance_id>[^/]+)/latestlog/(?P<length>\d+)/$','latest_log',name='latest_log'),
)