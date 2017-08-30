from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin

from .views import ( OfficeInspectionListView, OfficeInspectionDetailView, OfficeInspectionCreateView,
	DailyInspectionListView, DailyInspectionDetailView, DailyInspectionCreateView, shelf_inspection_ListView,
	shelf_inspection_DetailView)

urlpatterns = [
    url(r'^officeinspection$', OfficeInspectionListView.as_view(), name='OfficeInspection_list'),
    url(r'^officeinspection/create$', OfficeInspectionCreateView.as_view(), name='OfficeInspection_create'),
    url(r'^officeinspection/(?P<pk>\d+)/$', OfficeInspectionDetailView.as_view(), name='OfficeInspection_detail'), 
    url(r'^dailyinspection$', DailyInspectionListView.as_view(), name='dailyinspection_list'),
    url(r'^dailyinspection/create$', DailyInspectionCreateView.as_view(), name='dailyinspection_create'),
    url(r'^dailyinspection/(?P<pk>\d+)/$', DailyInspectionDetailView.as_view(), name='dailyinspection_detail'),   
    url(r'^shelfinspectionlist$', shelf_inspection_ListView.as_view(), name='shelf_inspection_list'),  
    url(r'^shelfinspectiondetail/(?P<pk>\d+)/$', shelf_inspection_DetailView.as_view(), name='shelf_inspection_detail'),  
]