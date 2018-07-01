from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin

from .views import (
    personalcenter_home, 
    myorder, 
    myuser_profile_extend, 
    ProfileDetailView
    )
from .views import (
    account_link_to_wechat, 
    account_unlink_from_wechat
    )
#from .views import upload_file, upload_status

urlpatterns = [

    url(r'^(?P<id>\d+)/$', personalcenter_home, name='personalcenter'),
    url(r'^(?P<id>\d+)/myorder$', myorder, name='myorder'), 
    url(r'^(?P<id>\d+)/myprofileextend$', myuser_profile_extend, name='myuser_profile_extend'),     
    url(r'^(?P<id>\d+)/change$', ProfileDetailView.as_view(), name='profile_detail'),  

    url(r'^linktowechat$', account_link_to_wechat, name='link_to_wechat'),
    url(r'^unlinkfromwechat$', account_unlink_from_wechat, name='unlink_from_wechat'),       
]