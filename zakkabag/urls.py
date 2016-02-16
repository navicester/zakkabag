from django.conf.urls import patterns, include, url
from zakkabag.views import handleRequest

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
	url(r'^$', handleRequest),
    url(r'^weixin', handleRequest),
    url(r'^debug', 'debug.views.handleDebug', name='handleDebug'),

    # url(r'^$', 'zakkabag.views.home', name='home'),
    # url(r'^zakkabag/', include('zakkabag.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

'''
urlpatterns += patterns('',
    url(r'^zakkabag/',include('zakkabag.urls')),
)
'''

