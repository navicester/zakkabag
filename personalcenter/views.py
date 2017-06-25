from django.shortcuts import render, get_object_or_404
from django.http import Http404, JsonResponse, HttpResponse
from django.contrib import auth
from .models import WechatUserProfile, UserProfile
from products.models import Product
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormMixin
from orders.models import Order
from .forms import MyUserForm, UploadFileForm
from django.core.cache import cache
from django.core.cache.backends.memcached import MemcachedCache
import json
from django.conf import settings
from django.utils.text import slugify

from orders.models import UserCheckout

from django.contrib.auth import get_user_model
UserModel = get_user_model()

# Create your views here.
def personalcenterhome(request,id):
    '''    
    try:
        myuser = UserModel.objects.get(id=id)
    except UserModel.DoesNotExist:
        raise Http404
    except:
        raise Http404
    '''
    myuser = get_object_or_404(UserModel, id=id)

    wechat = None
    try:
        wechat = WechatUserProfile.objects.get(user=myuser)
    except:
        pass


    template = "personalcenter/personalcenterhome.html"
    context = {    
        "myuser": myuser,
        'wechat': wechat,
        'product' : Product.objects.all()[0],   
    }

    return render(request, template, context)

def myorder(request,id):

    myuser = get_object_or_404(UserModel, id=id)
    try:
        usercheckout = UserCheckout.objects.get(user = myuser)
    except UserCheckout.DoesNotExist:
        usercheckout = None
    except:
        raise Http404
        
    order_objects = Order.objects.filter(user = usercheckout)

    template = "personalcenter/myorder.html"
    context = {    
        "myuser": myuser,
        "order_objects" : order_objects,
    }

    return render(request, template, context)

def myuser_profile_extend(request,id):

    myuser = get_object_or_404(UserModel, id=id)

    userprofle, created = UserProfile.objects.get_or_create(user = myuser)

    template = "personalcenter/profile_extend.html"
    context = {    
        "myuser": myuser,
        "userprofle" : userprofle,

    }

    return render(request, template, context)

def account_link_to_wechat(request):
    user = auth.get_user(request)
    wechat_id = request.session.get("wechat_id")
    wechat = None
    if wechat_id:
        try:
            wechat = WechatUserProfile.objects.get(pk=wechat_id)
            wechat.user = user
            wechat.save()
            return redirect(reverse("home", kwargs={}))
        except:
            pass

    return redirect(reverse("home", kwargs={}))

def account_unlink_from_wechat(request):
    wechat_id = request.session.get("wechat_id")
    wechat = None
    if wechat_id:
        try:
            wechat = WechatUserProfile.objects.get(pk=wechat_id)
            wechat.user = None
            wechat.save()
            #wechat profile without user is NOT allowed, so delete the wechat profile
            #but if deleted, it will become anomymous user (llead to auth.login fail),otherwise none when login with wechat again
            #wechat.delete()
            #request.session.delete(wechat_id)
        except:
            pass

    if request.is_ajax():
        data = {'unlink' : True }
        return JsonResponse(data)

    return redirect(reverse("home", kwargs={}))


def upload_file(request):
    print "upload_file"
    if request.method == 'POST':
        upload_form = UploadFileForm(request.POST, request.FILES)
        if upload_form.is_valid():
            filename=request.FILES['image']
            from PIL import Image
            if filename:
                img = Image.open(filename)
                import os
                photopath = os.path.join(settings.MEDIA_ROOT, 'upload')
                if not os.path.exists(photopath):
                    os.makedirs(photopath)
                img.save(os.path.join(photopath, filename.name))
                cache.set('cache_key_upload',os.path.join('upload', filename.name) ,60*15)
            return HttpResponse(json.dumps({'message': 'Upload complete!','url': os.path.join('upload', filename.name)}))
        else:
            return HttpResponse(json.dumps({'message': 'invalid form!'}))
    else:
        form = UploadFileForm()
        #return render_to_response('index.html', {'form': form}, context_instance=RequestContext(request))
        return HttpResponse(json.dumps({'message': 'invalid form!'}))

def upload_status(request):
    print "upload_status"
    if request.method == 'GET':
        if request.GET['key']:
            if cache.get(request.GET['key']):
                value = cache.get(request.GET['key'])
                return HttpResponse(json.dumps(value), content_type="application/json")
            else:
                return HttpResponse(json.dumps({'error':"No csrf value in cache"}), content_type="application/json")
        else:
            return HttpResponse(json.dumps({'error':'No parameter key in GET request'}), content_type="application/json")
    else:
        return HttpResponse(json.dumps({'error':'No GET request'}), content_type="application/json")

class ProfileDetailView(FormMixin, DetailView):
    model = UserModel
    template_name = "personalcenter/profile_detail.html"
    form_class = MyUserForm

    def get_context_data(self, *args, **kwargs):
        context = super(ProfileDetailView, self).get_context_data(*args, **kwargs)
        context["form"] = self.form_class(instance = self.get_object()) 
        upload_file_form = UploadFileForm()
        #upload_file_form.fields['image'].queryset = self.get_object(*args, **kwargs).image
        context["upload_form"] = upload_file_form

        usermodel = UserModel.objects.get(id=self.kwargs.get("id"))
        if UserCheckout.objects.filter(user = usermodel):
            usercheckout = UserCheckout.objects.get(user = usermodel)
            context["object_list"] = Order.objects.filter(user = usercheckout)

        return context

    def get_object(self, *args, **kwargs):
        user_pk = self.kwargs.get("id")
        usemodel = None
        if user_pk:
            usemodel = get_object_or_404(UserModel, pk=user_pk)
        return usemodel 

    def get_success_url(self):
        return reverse("personalcenter", kwargs=self.kwargs)    

    def post(self, request, *args, **kwargs):
        form = self.get_form() 
        #OR
        # form = self.form_class(request.POST, request.FILES)

        if form.is_valid():
            usermodel = UserModel.objects.get(id=self.kwargs.get("id"))
            usermodel.first_name = form.cleaned_data['first_name']
            usermodel.last_name = form.cleaned_data['last_name']
            usermodel.sex = form.cleaned_data['sex']
            usermodel.nickname = form.cleaned_data['nickname']
            usermodel.birthday = form.cleaned_data['birthday']

            # use plugin
            if 'image' in form.cleaned_data:
                usermodel.image = form.cleaned_data['image']
            #use ajax
            if not cache.get('cache_key_upload',None) is None:
                usermodel.image = cache.get('cache_key_upload',None)
                if cache.has_key('cache_key_upload'):
                    cache.delete('cache_key_upload')
            usermodel.save()
            return self.form_valid(form)
        else:
            self.object = self.get_object(*args, **kwargs)
            return self.form_invalid(form)

    def get(self, request, *args, **kwargs):  
        return super(ProfileDetailView, self).get(request, *args, **kwargs)          
