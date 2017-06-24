from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin

from .views import logout, login, GetVerificationCode
from .views import RegistrationView, ProfileUpdateView

urlpatterns = [

    url(r'^wechatlogin/$', 'wechat.views.wechatlogin', name='wechatlogin'), 
    url(r'^logout/$', logout, name='logout'), 
    url(r'^login/$', login, name='login'), 
    url(r'^register/$', RegistrationView.as_view(), name='register_phone'), 
    url(r'^completeProfile/(?P<pk>\d+)$', ProfileUpdateView.as_view(), name='profile_update'), 
    url(r'^getVerificationCode/$', GetVerificationCode, name='getVerificationCode'), 
]

