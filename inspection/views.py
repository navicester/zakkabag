from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.views.generic.edit import FormView, CreateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormMixin, ModelFormMixin
from django.http import HttpResponseRedirect
from django.conf import settings
from django.utils.translation import ugettext as _
from django_filters import FilterSet, CharFilter, NumberFilter
from django.db.models import Q

# Create your views here.
from .models import OfficeInspection, DailyInspection
from .forms import OfficeInspectionForm, DailyInspectionForm, InspectionFilterForm

# Create your views here.

def gen_qrcode(link):
    import qrcode
    qr=qrcode.QRCode(
         version = 2,
         error_correction = qrcode.constants.ERROR_CORRECT_L,
         box_size=10,
         border=10,)
    qr.add_data(link)
    qr.make(fit=True)
    img = qr.make_image()
    #img.show()

    from django.conf import settings
    import os
    photopath = os.path.join(settings.MEDIA_ROOT, "inspection")
    if not os.path.exists(photopath):
        os.makedirs(photopath)
    path = os.path.join(photopath, 'create.jpg')
    img.save(path)
    return path

class OfficeInspectionCreateView(CreateView):
    form_class = OfficeInspectionForm
    template_name = "inspection/officeinspection_create.html"

    def form_valid(self, form, *args, **kwargs):
        form = super(OfficeInspectionCreateView, self).form_valid(form, *args, **kwargs)
        return form

    def get_success_url(self, *args, **kwargs):
        return reverse("OfficeInspection_list", kwargs={}) 


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
        self.object = self.get_object(*args, **kwargs)

        if form.is_valid():
            return self.form_valid(form)
        else:            
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
        return reverse("OfficeInspection_list", kwargs={}) 

    def form_valid(self, form, *args, **kwargs):
        #form.instance = self.get_object(*args, **kwargs)  # without this, form will create another new object
        obj = form.save(commit = False)
        instance = self.get_object()
        obj.id = instance.id
        obj.timestamp = instance.timestamp
        obj.image = gen_qrcode(self.request.get_host() + reverse("OfficeInspection_create", kwargs={}))
        obj.save()

        return HttpResponseRedirect(self.get_success_url())

class OfficeInspectionListView(ListView): 
    model = OfficeInspection
    template_name = "dailyinspection/officeinspection_list.html"

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





class DailyInspectionCreateView(CreateView):
    form_class = DailyInspectionForm
    template_name = "dailyinspection/dailyinspection_create.html"

    def form_valid(self, form, *args, **kwargs):
        form = super(DailyInspectionCreateView, self).form_valid(form, *args, **kwargs)
        return form

    def get_success_url(self, *args, **kwargs):
        return reverse("dailyinspection_list", kwargs={}) 


class DailyInspectionDetailView(ModelFormMixin, DetailView):
    
    model = DailyInspection
    template_name = "dailyinspection/dailyinspection_detail.html"
    form_class = DailyInspectionForm

    def get_context_data(self, *args, **kwargs):
        context = super(DailyInspectionDetailView, self).get_context_data(*args, **kwargs)
        object = self.get_object()
        context["object"] =object 
        #selected = [item for item in object.impact]
        #initial=selected
        form = kwargs.get('form',None) # called in form_invalid
        if form is None:
            form = self.form_class(instance = self.get_object()) 
        context["form"] = form
        context["media"] = settings.MEDIA_URL
        return context        

    def get_object(self, *args, **kwargs):
        dailyinspection_pk = self.kwargs.get("pk")
        dailyinspection = None
        if dailyinspection_pk:
            print dailyinspection_pk
            dailyinspection = get_object_or_404(DailyInspection, pk=dailyinspection_pk)
        return dailyinspection 

    def get(self, request, *args, **kwargs):
        return super(DailyInspectionDetailView, self).get(request, *args, **kwargs) 

    def post(self, request, *args, **kwargs):
        form = self.get_form() 
        self.object = self.get_object(*args, **kwargs)

        if form.is_valid():
            return self.form_valid(form)
        else:            
            return self.form_invalid(form)

        return super(DailyInspectionDetailView, self).post(request, *args, **kwargs) 

    def dispatch(self, request, *args, **kwargs):
        instance = self.get_object()
        request.breadcrumbs([
            (_("Home"),reverse("home", kwargs={})),
            ("Daily Inspection",reverse("dailyinspection_list", kwargs={})),
            (instance,request.path_info),
        ])
        return super(DailyInspectionDetailView, self).dispatch(request,args,kwargs)   

    def get_success_url(self):
        return reverse("dailyinspection_list", kwargs={}) 

    def form_valid(self, form, *args, **kwargs):
        #form.instance = self.get_object(*args, **kwargs)  # without this, form will create another new object
        obj = form.save(commit = False)
        instance = self.get_object()
        obj.id = instance.id
        obj.created = instance.created
        if form.cleaned_data['image_before']:
            instance.image_before.delete(save=True)
            if form.clear_image_before_clear():
                obj.image_before = None
        else:
            if form.clear_image_before_clear() is None:
                obj.image_before = instance.image_before
            else:
                instance.image_before.delete(save=True)

        if form.cleaned_data['image_after']:
            instance.image_after.delete(save=True)
            if form.clear_image_after_clear():
                obj.image_after = None
        else:
            if form.clear_image_after_clear() is None:                
                obj.image_after = instance.image_after
            else:
                instance.image_after.delete(save=True)
        #obj.image = gen_qrcode(self.request.get_host() + reverse("dailyinspection_create", kwargs={}))
        obj.save()

        return HttpResponseRedirect(self.get_success_url())

class InsepctionFilter(FilterSet):
    cateory = CharFilter(name='cateory', lookup_type='icontains', distinct=True)
    #category_id = CharFilter(name='categories__id', lookup_type='icontains', distinct=True)
    correct_status = CharFilter(name='correct_status', lookup_type='icontains', distinct=True)
    owner = CharFilter(name='owner', lookup_type='icontains', distinct=True)

    class Meta:
        model = DailyInspection
        fields = [
            'owner',
            'correct_status',
            'cateory',
        ]

class FilterMixin(object):
    filter_class = None
    search_ordering_param = "ordering"

    def get_queryset(self, *args, **kwargs):
        try:
            qs = super(FilterMixin, self).get_queryset(*args, **kwargs)
            return qs
        except:
            raise ImproperlyConfigured("You must have a queryset in order to use the FilterMixin")

    def get_context_data(self, *args, **kwargs):
        context = super(FilterMixin, self).get_context_data(*args, **kwargs)
        qs = self.get_queryset()
        ordering = self.request.GET.get(self.search_ordering_param)
        if ordering:
            qs = qs.order_by(ordering)
        filter_class = self.filter_class
        if filter_class:
            f = filter_class(self.request.GET, queryset=qs)
            context["object_list"] = f
        return context

class DailyInspectionListView(FilterMixin, ListView): 
    model = DailyInspection
    template_name = "dailyinspection/dailyinspection_list.html"
    filter_class = InsepctionFilter

    def get_context_data(self, *args, **kwargs):
        context = super(DailyInspectionListView, self).get_context_data(*args, **kwargs)
        context["objects"] = DailyInspection.objects.all()
        context["objects_sort"] = DailyInspection.objects.order_by('-updated')
        context["query"] = self.request.GET.get("q")
        context["InspectionFilterForm"] = InspectionFilterForm(data=self.request.GET or None)        
        return context       

    def get_queryset(self, *args, **kwargs):
        qs = super(DailyInspectionListView, self).get_queryset(*args, **kwargs)
        query = self.request.GET.get("q")
        if query:
            qs = self.model.objects.filter(
                Q(impact__icontains=query) |
                Q(correct__icontains=query) |
                Q(owner__icontains=query) |
                Q(item__icontains=query)
                )
            try:
                qs2 = self.model.objects.filter(
                    Q(correct_status=query)
                )
                qs = (qs | qs2).distinct()
            except:
                pass
        return qs

    def dispatch(self, request, *args, **kwargs):
        request.breadcrumbs([
            (_("Home"),reverse("home", kwargs={})),
            (_('Daily Inspection'),request.path_info),
        ])
        return super(DailyInspectionListView, self).dispatch(request,args,kwargs)   
