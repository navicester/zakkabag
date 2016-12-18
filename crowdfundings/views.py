from django.shortcuts import render, render_to_response
from django.http import HttpResponse, JsonResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView, CreateView
from .models import Crowdfunding
from .forms import CrowdfundingCreateForm
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

class CrowdfundingCreateView(CreateView):
    template_name = 'crowdfundings/crowdfunding_create.html'
    form_class = CrowdfundingCreateForm
    success_url = "/crowdfunding"

    def get_context_data(self, *args, **kwargs):
        context = super(CrowdfundingCreateView, self).get_context_data(*args, **kwargs)
        # context["image_form"] = ProductImageForm()
        return context

    def get_form(self, *args, **kwargs):
        form = super(CrowdfundingCreateView, self).get_form(*args, **kwargs)

        # form.fields['categories'].queryset  = Category.objects.all()
        # form.fields['default'].queryset  = Category.objects.all()

        return form

    def post(self, request, *args, **kwargs):
        postresult = super(CrowdfundingCreateView, self).post(request, *args, **kwargs)

        # if 0:
        #     filename=request.FILES['image']
        #     from PIL import Image 
        #     if filename:
        #         img=Image.open(filename)
        #         title = self.object.title
        #         slug = slugify(title)
        #         basename, file_extension = filename.name.split(".")
        #         new_filename = "%s-%s.%s" %(slug, self.object.id, file_extension)
        #         from django.conf import settings
        #         import os
        #         photoname = os.path.join("products", slug, new_filename)
        #         photopath = os.path.join(settings.MEDIA_ROOT, "products", slug)
        #         if not os.path.exists(photopath):
        #             os.makedirs(photopath)
        #         img.save(os.path.join(settings.MEDIA_ROOT, photoname))
        #         ProductImage.objects.create(product = self.object, 
        #             image = photoname)

        # # BELOW ALSO WORKS
        # else:
        #     imageForm = ProductImageForm(request.POST, request.FILES)
        #     if imageForm.is_valid():
        #         productImage = imageForm.save(commit=False) 
        #         productImage.product = self.object
        #         productImage.save()
        #         return postresult

        return postresult              

def CommentsShow(request, pk=''):
    crowdfunding = Crowdfunding.objects.get(id=pk)
    context={
        'object': crowdfunding,
    }

    #return render_to_response('crowdfundings/comments_tree.html', {"object": crowdfunding})
    return render(request, "crowdfundings/comments_render.html", context)
    #return render(request, "crowdfundings/comments_tree.html", context)
    
