from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.contrib import auth
from .models import WechatUserProfile
from products.models import Product
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormMixin
from orders.models import Order
from .forms import MyUserForm

from django.contrib.auth import get_user_model
UserModel = get_user_model()

# Create your views here.
def personalcenterhome(request,id):

    wechatuser = get_object_or_404(UserModel, id=id)
    wechat = None
    try:
        wechatuser = UserModel.objects.get(id=id)
    except UserModel.DoesNotExist:
        raise Http404
    except:
        raise Http404

    try:
        wechat = WechatUserProfile.objects.get(user=wechatuser)
    except:
        pass


    template = "personalcenter/personalcenterhome.html"
    context = {    
        "object": wechatuser,
        'wechat': wechat,
        'product' : Product.objects.all()[0],   
    }

    return render(request, template, context)

def myorder(request,id):

    wechatuser = get_object_or_404(UserModel, id=id)
    try:
        wechatuser = UserModel.objects.get(id=id)
    except UserModel.DoesNotExist:
        raise Http404
    except:
        raise Http404

    order_objects = Order.objects.filter(user__id=wechatuser.id)

    template = "personalcenter/myorder.html"
    context = {    
        "object": wechatuser,
        "order_objects" : order_objects,

    }


    return render(request, template, context)

def accountlinktowechat(request):
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


class ProfileDetailView(FormMixin, DetailView):
    model = UserModel
    template_name = "personalcenter/profile_detail.html"
    form_class = MyUserForm

    # def dispatch(self, request, *args, **kwargs):
    #     if request.method == 'GET':
    #         pass
    #     else:
    #         pass
    #     return super(ProfileDetailView, self).dispatch(request, *args, **kwargs)


    def get_context_data(self, *args, **kwargs):
        context = super(ProfileDetailView, self).get_context_data(*args, **kwargs)
        context["form"] = MyUserForm(instance = self.get_object())
        return context

    def get_object(self, *args, **kwargs):
        user_pk = self.kwargs.get("id")
        usemodel = None
        if user_pk:
            usemodel = get_object_or_404(UserModel, pk=user_pk)
        return usemodel 

    # def get_form(self, *args, **kwargs):
    #     form = super(ProfileDetailView, self).get_form(*args, **kwargs)
    #     return form

    # def form_invalid(self, form):
    #     return self.render_to_response(self.get_context_data(form=form))        

    def get_success_url(self):
        return reverse("personalcenter", kwargs=self.kwargs)    

    def post(self, request, *args, **kwargs):
        # form = self.get_form()
        form = form = self.form_class(request.POST, request.FILES)

        if form.is_valid():
            usermodel = UserModel.objects.get(id=self.kwargs.get("id"))
            usermodel.first_name = form.cleaned_data['first_name']
            usermodel.last_name = form.cleaned_data['last_name']
            #if hasattr(form.cleaned_data, 'image'):
            if 'image' in form.cleaned_data:
                usermodel.image = form.cleaned_data['image']
            usermodel.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get(self, request, *args, **kwargs):  
        return super(ProfileDetailView, self).get(request, *args, **kwargs)          

