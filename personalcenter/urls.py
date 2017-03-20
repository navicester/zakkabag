from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin

from .views import personalcenterhome, accountlinktowechat, account_unlink_from_wechat, myorder, ProfileDetailView

urlpatterns = [
    # Examples:

    url(r'^(?P<id>\d+)/$', personalcenterhome, name='personalcenter'),
    url(r'^(?P<id>\d+)/myorder$', myorder, name='myorder'),
    url(r'^linktowechat$', accountlinktowechat, name='link_to_wechat'),
    url(r'^unlinkfromwechat$', account_unlink_from_wechat, name='unlink_from_wechat'),    
    # url(r'^create$', ProductCreateView.as_view(), name='products_create'),
    url(r'^(?P<id>\d+)/change$', ProfileDetailView.as_view(), name='profile_detail'),
    # #url(r'^(?P<id>\d+)', 'products.views.product_detail_view_func', name='product_detail_function'),
    # url(r'^(?P<pk>\d+)/inventory/$', VariationListView.as_view(), name='product_inventory'),    
]