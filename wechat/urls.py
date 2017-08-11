from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin

from .views import handleRequest
from .debug import handleDebug
from .menu import handleMenuRequest

urlpatterns = [
    url(r'^weixin', 'wechat.views.handleRequest'),
    url(r'^menu', 'wechat.menu.handleMenuRequest', name='handleMenuRequest'),
    url(r'^debug', 'wechat.debug.handleDebug', name='handleDebug'),
]