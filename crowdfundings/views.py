from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import Crowdfunding
from .mixins import StaffRequiredMixin
import json

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

class CrowdfundingDetailView(DetailView):
    model = Crowdfunding
    def get_context_data(self, *args, **kwargs):
        context = super(CrowdfundingDetailView, self).get_context_data(*args, **kwargs)
        obj = self.get_object()
        # product_set = obj.product_set.all()
        # default_products = obj.default_category.all()
        # products = ( product_set | default_products ).distinct()
        # context["products"] = products
        # context["categories"] = Category.objects.all()
        return context        

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        if request.is_ajax():
            if "addFavorite" == request.GET.get("purpose", 'addFavorite'):                
                if True == obj.is_favorite:
                    obj.is_favorite = False
                else:
                    obj.is_favorite = True
                obj.save()
                data = {       
                        "is_favorite": obj.is_favorite,                          
                        }

                return JsonResponse(data) 
        else:
            return super(CrowdfundingDetailView, self).get(request, *args, **kwargs) 