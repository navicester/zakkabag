from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin

from .views import CrowdfundingListView, CrowdfundingDetailView

urlpatterns = [

    url(r'^$', CrowdfundingListView.as_view(), name='CrowdfundingListView'),
    # url(r'^create$', ProductCreateView.as_view(), name='products_create'),
    url(r'^(?P<pk>\d+)/$', CrowdfundingDetailView.as_view(), name='Crowdfunding_detail'),
    url(r'^comments/', include('django_comments.urls')),
    # url(r'^(?P<pk>\d+)/inventory/$', VariationListView.as_view(), name='product_inventory'),   
    # url(r'^exchangerule$',
    #     TemplateView.as_view(template_name='products/exchange_rule.html'),
    #     name='exchange_rule'),     
]