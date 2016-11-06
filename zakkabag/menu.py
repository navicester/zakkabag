
from django.http import HttpResponse
from django.shortcuts import render

def handleMenuRequest(request):
	if request.method == 'GET':
		return render(request, "menu.html", {})
	elif request.method == 'POST':
		pass
	else:
		return "welcome to zakkabag"
