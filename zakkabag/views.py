from django.shortcuts import render

def about(request):
	return render(request, "about.html", {})


def sitemap(request):
    return render(request, "map.html", {})	