from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin

from .views import personalcenterhome, accountlinktowechat, account_unlink_from_wechat, myorder, ProfileDetailView
from .views import upload_file, upload_status

urlpatterns = [
    # Examples:

    url(r'^(?P<id>\d+)/$', personalcenterhome, name='personalcenter'),
    url(r'^(?P<id>\d+)/myorder$', myorder, name='myorder'),
    url(r'^linktowechat$', accountlinktowechat, name='link_to_wechat'),
    url(r'^unlinkfromwechat$', account_unlink_from_wechat, name='unlink_from_wechat'),    
    url(r'^(?P<id>\d+)/change$', ProfileDetailView.as_view(), name='profile_detail'),
    url(r'^uploadfile', upload_file, name='upload_file'),
    url(r'^upload_status$', upload_status, name='upload_status'),
]