from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin

from .views import OfficeInspectionListView, OfficeInspectionDetailView

urlpatterns = [
    url(r'^$', OfficeInspectionListView.as_view(), name='OfficeInspection_list'),
    url(r'^(?P<pk>\d+)/$', OfficeInspectionDetailView.as_view(), name='OfficeInspection_detail'), 
]