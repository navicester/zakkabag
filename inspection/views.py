from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.views.generic.edit import FormView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormMixin, ModelFormMixin


# Create your views here.
from .models import OfficeInspection
from .forms import OfficeInspectionForm

# Create your views here.
'''
class OfficeInspectionFormView(FormView):
    form_class = AddressForm
    template_name = "inspection/office_inspection.html"

    def get_form(self, *args, **kwargs):
        form = super(OfficeInspectionFormView, self).get_form(*args, **kwargs)

        form.fields["billing_address"].queryset = UserAddress.objects.filter(
                user__email=self.request.user.email,
                type='billing',
            )
        form.fields["shipping_address"].queryset = UserAddress.objects.filter(
                user__email=self.request.user.email,
                type='shipping',
            )
        print self.request.user.email
        return form

    def form_valid(self, form, *args, **kwargs):
        form = super(OfficeInspectionFormView, self).form_valid(form, *args, **kwargs)
        return form

    def get_success_url(self, *args, **kwargs):
        return "/home/"
'''

#class OfficeInspectionDetailView(FormMixin, DetailView):
class OfficeInspectionDetailView(ModelFormMixin, DetailView):
    
    model = OfficeInspection
    template_name = "inspection/officeinspection_detail.html"
    form_class = OfficeInspectionForm

    def get_context_data(self, *args, **kwargs):
        context = super(OfficeInspectionDetailView, self).get_context_data(*args, **kwargs)
        context["object"] = self.get_object()
        context["form"] = self.form_class(instance = self.get_object()) 
        return context        

    def get_object(self, *args, **kwargs):
        officeinspection_pk = self.kwargs.get("pk")
        officeinspection = None
        if officeinspection_pk:
            print officeinspection_pk
            officeinspection = get_object_or_404(OfficeInspection, pk=officeinspection_pk)
        return officeinspection 

    def get(self, request, *args, **kwargs):
        return super(OfficeInspectionDetailView, self).get(request, *args, **kwargs) 

    def post(self, request, *args, **kwargs):
        form = self.get_form() 

        if form.is_valid():
            return self.form_valid(form)
        else:
            self.object = self.get_object(*args, **kwargs)
            return self.form_invalid(form)

        return super(OfficeInspectionDetailView, self).post(request, *args, **kwargs) 

    def dispatch(self, request, *args, **kwargs):
        instance = self.get_object()
        request.breadcrumbs([
            ("Home",reverse("home", kwargs={})),
            ("Inspection",reverse("OfficeInspection_list", kwargs={})),
            (instance,request.path_info),
        ])
        return super(OfficeInspectionDetailView, self).dispatch(request,args,kwargs)   

    def get_success_url(self):
        return reverse("OfficeInspection_list", kwargs=self.kwargs)    

class OfficeInspectionListView(ListView): 
    model = OfficeInspection
    template_name = "inspection/officeinspection_list.html"

    def get_context_data(self, *args, **kwargs):
        context = super(OfficeInspectionListView, self).get_context_data(*args, **kwargs)
        context["objects"] = OfficeInspection.objects.all()
        context["objects_sort"] = OfficeInspection.objects.order_by('-updated')
        return context       

    def dispatch(self, request, *args, **kwargs):
        request.breadcrumbs([
            ("Home",reverse("home", kwargs={})),
            ('Inspection',request.path_info),
        ])
        return super(OfficeInspectionListView, self).dispatch(request,args,kwargs)   
