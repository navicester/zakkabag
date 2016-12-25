from django.conf import settings
from django.conf.urls.static import static

from django.conf.urls import patterns, include, url
from wechat.views import handleRequest
from wechat.menu import handleMenuRequest


from django.contrib import admin

from carts.views import CartView, ItemCountView, CheckoutView, CheckoutFinalView
from orders.views import (
                    AddressSelectFormView, 
                    UserAddressCreateView, 
                    OrderList, 
                    OrderDetail)
					
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
	url(r'^$', 'wechat.views.handleRequest'),
    url(r'^weixin', 'wechat.views.handleRequest'),
    url(r'^menu', 'wechat.menu.handleMenuRequest', name='handleMenuRequest'),
    url(r'^debug', 'debug.views.handleDebug', name='handleDebug'),

    url(r'^home$', 'newsletter.views.home', name='home'),
    url(r'^contact/$', 'newsletter.views.contact', name='contact'),   
    url(r'^about/$', 'zakkabag.views.about', name='about'),



    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),


    url(r'^admin/', include(admin.site.urls)),

    url(r'^accounts/', include('registration.backends.default.urls')),    
    url(r'^products/', include('products.urls')),
    url(r'^categories/', include('products.urls_categories')),

    url(r'^orders/$', OrderList.as_view(), name='orders'),
    url(r'^orders/(?P<pk>\d+)/$', OrderDetail.as_view(), name='order_detail'),

    url(r'^cart/$', CartView.as_view(), name='cart'), 
    url(r'^cart/count/$', ItemCountView.as_view(), name='item_count'),  

    url(r'^checkout/$', CheckoutView.as_view(), name='checkout'),    
    url(r'^checkout/address/$', AddressSelectFormView.as_view(), name='order_address'),   
    url(r'^checkout/address/add/$', UserAddressCreateView.as_view(), name='user_address_create'), 
    url(r'^checkout/final/$', CheckoutFinalView.as_view(), name='checkout_final'),   	

    url(r'^wechatlogin/$', 'wechat.views.wechatlogin', name='wechatlogin'), 
    url(r'^logout/$', 'newsletter.views.logout', name='logout'), 
    url(r'^login/$', 'newsletter.views.login', name='login'), 

    url(r'^personalcenter/', include('personalcenter.urls')),
    url(r'^crowdfundings/', include('crowdfundings.urls')),

    # url(r'^articles/comments/', include('django_comments.urls')),
)

'''
urlpatterns += patterns('',
    url(r'^zakkabag/',include('zakkabag.urls')),
)
'''

if settings.DEBUG:
	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)