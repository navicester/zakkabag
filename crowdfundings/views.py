from django.shortcuts import render
from django.views.generic.list import ListView
from .models import Crowdfunding
from .mixins import StaffRequiredMixin

# Create your views here.
class CrowdfundingListView(ListView, StaffRequiredMixin):
    model = Crowdfunding
    queryset = Crowdfunding.objects.all()

    def get_context_data(self, *args, **kwargs):
        context = super(CrowdfundingListView, self).get_context_data(*args, **kwargs)
        # context["now"] = timezone.now()     
        return context

    def get_queryset(self, *args, **kwargs):
        return  super(CrowdfundingListView, self).get_queryset(*args, **kwargs)