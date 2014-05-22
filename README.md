#OpenStack User Dashboard
This is the openstack dashboard for the common users. It is like below:
![image] (https://raw.github.com/ShenMinwei/OpenstackUserDashboard/master/screenshots/1.png)
And when you open the console, you will see:
![image] (https://raw.github.com/ShenMinwei/OpenstackUserDashboard/master/screenshots/2.png)
The instance panel is collapsible:
![image] (https://raw.github.com/ShenMinwei/OpenstackUserDashboard/master/screenshots/3.png)
And ceilometer support is also included:
![image] (https://raw.github.com/ShenMinwei/OpenstackUserDashboard/master/screenshots/4.png)

##How to use
###Ubuntu
1. copy openstack_dashboard to /usr/share/openstack-dashboard
2. copy policy.json to /etc/keystone
3. copy user.py to /etc/share/pyshared/openstack_auth
4. restart the server
5. create a role 'user' and assign it to someone like 'Tom'
6. log in as 'Tom', you will see the dashboard

