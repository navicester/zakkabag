from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin

from .views import ( OfficeInspectionListView, OfficeInspectionDetailView, OfficeInspectionCreateView,
	DailyInspectionListView, DailyInspectionDetailView, DailyInspectionCreateView, shelf_inspectionView,
	shelf_inspectionListView)

urlpatterns = [
    url(r'^officeinspection$', OfficeInspectionListView.as_view(), name='OfficeInspection_list'),
    url(r'^officeinspection/create$', OfficeInspectionCreateView.as_view(), name='OfficeInspection_create'),
    url(r'^officeinspection/(?P<pk>\d+)/$', OfficeInspectionDetailView.as_view(), name='OfficeInspection_detail'), 
    url(r'^dailyinspection$', DailyInspectionListView.as_view(), name='dailyinspection_list'),
    url(r'^dailyinspection/create$', DailyInspectionCreateView.as_view(), name='dailyinspection_create'),
    url(r'^dailyinspection/(?P<pk>\d+)/$', DailyInspectionDetailView.as_view(), name='dailyinspection_detail'),   
    url(r'^shelfinspection$', shelf_inspectionView.as_view(), name='shelf_inspection'),  
    url(r'^shelf_inspectionList/(?P<pk>\d+)/$', shelf_inspectionListView.as_view(), name='shelf_inspectionList'),  
]