function showConsole(url,name){
	var label = document.getElementById("consoleLabel");
	label.innerHTML=name;
	$("#console_embed").attr("src",url)
	$("#view_console_window").attr("href",url)
}

function get_ajax_request(){
	var x;
	if (window.XMLHttpRequest)
		x =new XMLHttpRequest();
	else
		x =new ActiveXObject("Microsoft.XMLHTTP");

	return x;
}

function stopInstance(id){
	var xmlhttp = get_ajax_request();

	xmlhttp.open("GET",id+"/stopinstance",true);
	xmlhttp.send();

	var table = document.getElementById(id).getElementsByTagName('tbody')[0]
	table.getElementsByTagName('tr')[1].getElementsByTagName('td')[1].innerHTML = "STOPPING";

	xmlhttp.onreadystatechange=function(){
		if (xmlhttp.readyState==4){
			var result = xmlhttp.responseText;
			var data=eval("("+result+")");
			if(data.status == "error"){
				console.log("error")
				var x = document.getElementsByName("info_board_error")[0];
				x.getElementsByTagName('p')[0].innerHTML = data.message;
				x.style.display = 'block'
			}
			else{
				console.log("success")
				var x = document.getElementsByName("info_board_success")[0];
				x.getElementsByTagName('p')[0].innerHTML = data.message;
				x.style.display = 'block';
				renewInstance(id);
			}
		}

	}
}

function startInstance(id){
	var xmlhttp = get_ajax_request();

	var table = document.getElementById(id).getElementsByTagName('tbody')[0]
	table.getElementsByTagName('tr')[1].getElementsByTagName('td')[1].innerHTML = "STARTING";

	xmlhttp.onreadystatechange=function(){
		if (xmlhttp.readyState==4){
			var result = xmlhttp.responseText;
			var data=eval("("+result+")");
			if(data.status == "error"){
				var x = document.getElementsByName("info_board_error")[0];
				x.getElementsByTagName('p')[0].innerHTML = data.message;
				x.style.display = 'block'
			}
			else{
				var x = document.getElementsByName("info_board_success")[0];
				x.getElementsByTagName('p')[0].innerHTML = data.message;
				x.style.display = 'block';
				renewInstance(id);
			}
		}

	} 
	xmlhttp.open("GET",id+"/startinstance",true);
	xmlhttp.send();
}

function suspendInstance(id){
	var xmlhttp = get_ajax_request();
	if (window.XMLHttpRequest)
		xmlhttp=new XMLHttpRequest();
	else
		xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");

	var table = document.getElementById(id).getElementsByTagName('tbody')[0]
	table.getElementsByTagName('tr')[1].getElementsByTagName('td')[1].innerHTML = "SUSPENDING";

	xmlhttp.onreadystatechange=function(){
		if (xmlhttp.readyState==4){
			var result = xmlhttp.responseText;
			var data=eval("("+result+")");
			if(data.status == "error"){
				var x = document.getElementsByName("info_board_error")[0];
				x.getElementsByTagName('p')[0].innerHTML = data.message;
				x.style.display = 'block'
			}
			else{
				var x = document.getElementsByName("info_board_success")[0];
				x.getElementsByTagName('p')[0].innerHTML = data.message;
				x.style.display = 'block';
				renewInstance(id);
			}
		}

	} 
	xmlhttp.open("GET",id+"/suspendinstance",true);
	xmlhttp.send();
}

function resumeInstance(id){
	var xmlhttp = get_ajax_request();
	var table = document.getElementById(id).getElementsByTagName('tbody')[0]
	table.getElementsByTagName('tr')[1].getElementsByTagName('td')[1].innerHTML = "RESUMING";

	xmlhttp.onreadystatechange=function(){
		if (xmlhttp.readyState==4){
			var result = xmlhttp.responseText;
			var data=eval("("+result+")");
			if(data.status == "error"){
				var x = document.getElementsByName("info_board_error")[0];
				x.getElementsByTagName('p')[0].innerHTML = data.message;
				x.style.display = 'block'
			}
			else{
				var x = document.getElementsByName("info_board_success")[0];
				x.getElementsByTagName('p')[0].innerHTML = data.message;
				x.style.display = 'block';
				renewInstance(id);
			}
			
		}

	} 
	xmlhttp.open("GET",id+"/resumeinstance",true);
	xmlhttp.send();
}

function renewInstance(id){
	var x = get_ajax_request();

	x.onreadystatechange=function(){
		if (x.readyState==4){
			var result = x.responseText;
			var data=eval("("+result+")");
			var table = document.getElementById(id).getElementsByTagName('tbody')[0]
			table.getElementsByTagName('tr')[1].getElementsByTagName('td')[1].innerHTML = data.status;
			table.getElementsByTagName('tr')[2].getElementsByTagName('td')[1].innerHTML = data.powerstate;
		}

	} 
	x.open("GET",id+"/renewinstance",true);
	x.send();		
}

function closeInfoBoard(name){
	var x = document.getElementsByName(name)[0];
	x.style.display = 'none'
}

function validateForm(){
	var psd = document.getElementsByName("password")[0].value;
	var con_psd = document.getElementsByName("confirm_password")[0].value;
	var email = document.getElementsByName("email")[0].value;
	var atpos = email.indexOf("@");
	var dotpos = email.lastIndexOf(".");

	if (atpos < 1 || dotpos < atpos +2 || dotpos+2 >= email.length){
		var x = document.getElementsByName("error_message")[0];
		x.innerHTML = "Invalid email adress!"
		x.style.color = '#ff0000'
		return false;
	}

	if(psd != con_psd){
		var x= document.getElementsByName("error_message")[0];
		x.innerHTML = "Confirm password is different from password!"
		x.style.color = '#ff0000'
		return false;
	}
	return true;
}

//control the antion buttons
function checkStatus(id){
	var table = document.getElementById(id).getElementsByTagName('tbody')[0];
	var status = table.getElementsByTagName('tr')[1].getElementsByTagName('td')[1].innerHTML;
	var powerstate = table.getElementsByTagName('tr')[2].getElementsByTagName('td')[1].innerHTML;
	if(status == "ACTIVE"){
		$("#start-instance-button-"+id).hide();
		$("#stop-instance-button-"+id).show();
		$("#suspend-instance-button-"+id).show();
		$("#resume-instance-button-"+id).hide();
	}
	else if (status == "SHUTOFF"){
		$("#start-instance-button-"+id).show();
		$("#stop-instance-button-"+id).hide();
		$("#suspend-instance-button-"+id).hide();
		$("#resume-instance-button-"+id).hide();
	}
	else if(status == "SUSPENDED"){
		$("#start-instance-button-"+id).hide();
		$("#stop-instance-button-"+id).hide();
		$("#suspend-instance-button-"+id).hide();
		$("#resume-instance-button-"+id).resume();
	}
}

//get statistics and draw the cpu chart
function get_cpu_statistics(id,period,init){
	if(init==true){
		document.getElementById('cpu_'+id).getElementsByTagName("select")[0].getElementsByTagName('option')[0].selected='selected';
	}
	var url = id+"/getcpustatistics/"+period;
	var x = get_ajax_request();
	x.open("GET",url,true);
	x.send();

	x.onreadystatechange=function(){
		if (x.readyState==4){
			var result = x.responseText;
			var data=eval("("+result+")");
			draw_cpu_chart(data,id);
		}				
	} 	
}

function draw_cpu_chart(statistics,id){
	var div_id = 'cpu_'+id+'_chart';
	document.getElementById(div_id).innerHTML="";
	new Morris.Line({
		element: div_id,
		data: statistics.cpu,
		xkey: 'duration_start',
		ykeys: ['avg'],
		labels: ['CPU avg(e^12)']
	});
}

//get statistics and draw the network chart
function get_network_statistics(id,period,init){
	if(init==true){
		document.getElementById('network_'+id).getElementsByTagName("select")[0].getElementsByTagName('option')[0].selected='selected';
	}
	var x = get_ajax_request();
	var url = id+"/getnetworkstatistics/"+period;

	x.onreadystatechange=function(){
		if (x.readyState==4){
			var result = x.responseText;
			var data=eval("("+result+")");
			draw_network_chart(data,id);
		}

	} 
	x.open("GET",url,true);
	x.send();
}

function draw_network_chart(statistics,id){
	var div_id = "network_"+id+"_chart";
	document.getElementById(div_id).innerHTML="";

	var incoming_data = statistics.network_incoming_bytes;
	var outgoing_data = statistics.network_outgoing_bytes;
	var dataset = new Array();
	for(var i=0;i<incoming_data.length;i++){
		var data={duration_start:incoming_data[i].duration_start,incoming_avg:incoming_data[i].avg,outgoing_avg:outgoing_data[i].avg};
		dataset.push(data);
	}
	new Morris.Line({
		element: div_id,
		data: dataset,
		xkey: 'duration_start',
		ykeys: ['incoming_avg','outgoing_avg'],
		labels: ['incoming bytes(KB)','outgoing bytes(KB)']
	});
}

////get statistics and draw the disk chart
function get_disk_statistics(id,period,init){
	if (init == true){
		document.getElementById('disk_'+id).getElementsByTagName("select")[0].getElementsByTagName('option')[0].selected='selected'
	}
	var x = get_ajax_request();
	var url = id+"/getdiskstatistics/"+period;

	x.onreadystatechange=function(){
		if (x.readyState==4){
			var result = x.responseText;
			var data=eval("("+result+")");
			draw_disk_chart(data,id);
		}
	} 
	x.open("GET",url,true);
	x.send();
}

function draw_disk_chart(statistics,id){
	var div_id = "disk_"+id+"_chart";
	document.getElementById(div_id).innerHTML="";

	var read_data = statistics.disk_read_bytes;
	var write_data = statistics.disk_write_bytes;
	var dataset = new Array();
	for(var i=0;i<read_data.length;i++){
		var data={duration_start:read_data[i].duration_start,read_avg:read_data[i].avg,write_avg:write_data[i].avg};
		dataset.push(data);
	}
	new Morris.Line({
		element: div_id,
		data: dataset,
		xkey: 'duration_start',
		ykeys: ['read_avg','write_avg'],
		labels: ['read bytes(MB)','write bytes(MB)']
	});
}

function getLatestLog(id){
	var xmlhttp;
	if (window.XMLHttpRequest)
		xmlhttp=new XMLHttpRequest();
	else
		xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");

	xmlhttp.onreadystatechange=function(){
		if (xmlhttp.readyState==4){
			var pre = document.getElementsByTagName("pre")[0]
			pre.innerHTML = xmlhttp.responseText
		}
		
	} 
	length = document.getElementsByName("log_length")[0].value
	url  =  "../latestlog/"+length
	xmlhttp.open("GET",url,true);
	xmlhttp.send();
}

function viewFullLog(id){
	var xmlhttp;
	if (window.XMLHttpRequest)
		xmlhttp=new XMLHttpRequest();
	else
		xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");

	xmlhttp.onreadystatechange=function(){
		if (xmlhttp.readyState==4){
			var pre = document.getElementsByTagName("pre")[0]
			pre.innerHTML = xmlhttp.responseText
		}
		
	} 
	length = document.getElementsByName("log_length")[0].value
	url  =  "../fulllog/"
	xmlhttp.open("GET",url,true);
	xmlhttp.send();
}
