# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.template import RequestContext, Template
from django.views.decorators.csrf import csrf_exempt
from django.utils.encoding import smart_str, smart_unicode
from translate import paraseMsgXml,paraseYouDaoXml,getReplyXml
from django.shortcuts import render

import xml.etree.ElementTree as ET
import urllib,urllib2,hashlib

TOKEN = "zakkabag"

YOUDAO_KEY = "1228130126"
YOUDAO_KEY_FROM = "zakkabag"
YOUDAO_DOC_TYPE = "xml"

@csrf_exempt
def handleRequest(request):
	if request.method == 'GET':
		#response = HttpResponse(request.GET['echostr'],content_type="text/plain")
		response = HttpResponse(checkSignature(request),content_type="text/plain")
		return response
	elif request.method == 'POST':
		#c = RequestContext(request,{'result':responseMsg(request)})
		#t = Template('{{result}}')
		#response = HttpResponse(t.render(c),content_type="application/xml")
		response = HttpResponse(responseMsg(request),content_type="application/xml")
		return response
	else:
		#return None
		return "welcome to zakkabag"

def checkSignature(request):
	global TOKEN
	signature = request.GET.get("signature", None)
	timestamp = request.GET.get("timestamp", None)
	nonce = request.GET.get("nonce", None)
	echoStr = request.GET.get("echostr",None)

	token = TOKEN
	tmpList = [token,timestamp,nonce]
	tmpList.sort()
	tmpstr = "%s%s%s" % tuple(tmpList)
	tmpstr = hashlib.sha1(tmpstr).hexdigest()
	
	if tmpstr == signature:
		return echoStr
	else:
		return "checkSignature fail"

def responseMsg(request):
	rawStr = ''
	if request.method == 'GET':
		rawStr = smart_str(request.GET['send-content'].strip())		
	elif request.method == 'POST':
		rawStr = smart_str(request.raw_post_data)
		#rawStr = smart_str(request.POST['XML'])
	
	msg = paraseMsgXml(ET.fromstring(rawStr))
	
	queryStr = msg.get('Content','You have input nothing~')

	raw_youdaoURL = "http://fanyi.youdao.com/openapi.do?keyfrom=%s&key=%s&type=data&doctype=%s&version=1.1&q=" % (YOUDAO_KEY_FROM,YOUDAO_KEY,YOUDAO_DOC_TYPE)	
	youdaoURL = "%s%s" % (raw_youdaoURL,urllib2.quote(queryStr))

	req = urllib2.Request(url=youdaoURL)
	result = urllib2.urlopen(req).read()

	replyContent = paraseYouDaoXml(ET.fromstring(result))

	return getReplyXml(msg,replyContent)

def about(request):
	return render(request, "about.html", {})
