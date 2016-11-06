
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.encoding import smart_str, smart_unicode
import xml.etree.ElementTree as ET
import urllib2
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def handleMenuRequest(request):
	if request.method == 'GET':
		return render(request, "menu.html", {})
	elif request.method == 'POST':
		purpose = smart_str(request.POST.get("purpose", None))
		json_data = None
		if "get_token" == purpose:
			appid = smart_str(request.POST.get("appid", None))
			appsecret = smart_str(request.POST.get("appsecret", None))			
			get_token_url = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s" % (appid , appsecret);
			req = urllib2.Request(url=get_token_url)
			result = urllib2.urlopen(req).read()
			json_data = json.loads(result) #json-format string to json
		elif "delete_menu" == purpose:
			access_token = smart_str(request.POST.get("access_token", None))
			delete_menu_url = "https://api.weixin.qq.com/cgi-bin/menu/delete?access_token=%s" % (access_token);
			req = urllib2.Request(url=delete_menu_url)
			result = urllib2.urlopen(req).read()
			json_data = json.loads(result) #json-format string to json			
		else:
			pass

		#if request.GET.has_key('ajax'): 
		if request.is_ajax():
			try:
				response = HttpResponse(json.dumps(json_data),content_type="application/json")
				print response				
			except:
				response = HttpResponse("fail",content_type="application/xml")
			return response
		else:
			return render(request, "menu.html", {})
	else:
		return "welcome to zakkabag"
