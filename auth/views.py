from django.shortcuts import render, redirect
from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate#, login, logout
from django.contrib.auth import views as auth_views
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib import auth
from django.views.generic.edit import FormView, UpdateView
from zakkabag.settings import APP_ID, APP_SECRET
from weixin.client import WeixinMpAPI
from forms import UserUpdateForm
#from weixin.oauth2 import OAuth2AuthExchangeError

from django.utils.module_loading import import_string
REGISTRATION_FORM_PATH = getattr(settings, 'REGISTRATION_FORM','auth.forms.RegistrationForm')
REGISTRATION_FORM = import_string(REGISTRATION_FORM_PATH)

from django.contrib.auth import get_user_model
UserModel = get_user_model

#from django.contrib.auth.models import User
#http://www.cnblogs.com/smallcoderhujin/p/3193103.html


# Create your views here.
#refer to django/contrib/auth/views.py
#http://127.0.0.1:8000/accounts/activate/??
def login(request):
    REDIRECT_URI = request.POST.get('next', request.GET.get('next', reverse("home", kwargs={}))) #next indicated in templaetes
    if request.method == 'GET':
        code = request.GET.get('code')
        if code:
            redirect_to = "http://%s%s" % (request.META['HTTP_HOST'], reverse("home", kwargs={})) # redirection URL after authenticate
            api = WeixinMpAPI(appid=APP_ID, 
                        app_secret=APP_SECRET,
                        redirect_uri=redirect_to)
            auth_info = api.exchange_code_for_access_token(code=code)
            api = WeixinMpAPI(access_token=auth_info['access_token'])
            api_user = api.user(openid=auth_info['openid'])                
            user = authenticate(request=request, user=api_user)
            print user
            if user:
                auth_login(request, user)
                return redirect(redirect_to)

        return redirect(reverse("auth_login", kwargs={}))
    else:  #normal login is POST
        REDIRECT_FIELD_NAME = 'next'
        return auth_views.login(request, redirect_field_name=REDIRECT_FIELD_NAME, extra_context=None)    

        # below method is also OK
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request=request, username=username, password=password)
        if user is not None:
            auth_login(request, user)                
        else:
            return redirect(reverse("auth_login", kwargs={}))

    return auth_views.login(request, redirect_field_name=REDIRECT_URI, extra_context=None)    

def logout(request):
    try:
        del request.session['wechat_id']
    except:
        pass
    auth_logout(request)
    return redirect(reverse("home", kwargs={}))



class RegistrationView(FormView):
    form_class = REGISTRATION_FORM
    success_url = None
    template_name = 'auth/registration_form.html'

    #def dispatch(self, request, *args, **kwargs):
    #    return super(RegistrationView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
    	is_exist = UserModel().objects.filter(phone=form.cleaned_data['phone']).exists()
        #print is_exist
        users = UserModel().objects.filter(username=form.cleaned_data['phone'])
        #print users
        #print form.cleaned_data['phone']
        #if users :
            #from django import forms
            #raise forms.ValidationError('User Exist!')
            #return redirect(reverse("register_phone", kwargs={}))
            #return self.render_to_response(self.get_context_data(form=form))

        new_user = self.register(form)
        success_url = self.get_success_url(new_user)
        try:
            to, args, kwargs = success_url
        except ValueError:
            return redirect(success_url)
        else:
            return redirect(to, *args, **kwargs)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

    def register(self, form):
        if hasattr(form, 'save'):
            new_user_instance = form.save()
        else:
            #new_user_instance = (UserModel().objects.create_user(**form.cleaned_data))
            
            new_user_instance = (UserModel().objects.create_user(
                form.cleaned_data['phone'],
                'phone', 
                None,
                form.cleaned_data['password'],))
                
        
        return new_user_instance

    def get_success_url(self, user=None):
        #return super(RegistrationView, self).get_success_url()
        try:
            return reverse("profile_update", kwargs={'pk':user.id}) 
        except UserModel.DoesNotExist:
            return None 


import random

verificationCode = 0

def GetVerificationCode():
    verificationCode = random()

class ProfileUpdateView(UpdateView):
    model = UserModel
    form_class = UserUpdateForm
    template_name = 'auth/user_update_form.html'
    success_url = None

    def get_object(self, *args, **kwargs):
        try:
            return model.objects.get(id=kwargs.get('pk'))
        except:
            return None

    def get_form(self, form_class):
        #print self.get_form_kwargs()
        #return self.form_class(self.get_object(), **self.get_form_kwargs())     
        return self.form_class(self.get_object())  

    def post(self, request, *args, **kwargs):  
        postresult = super(ProfileUpdateView, self).post(request, *args, **kwargs)

        form = self.form_class(request.POST, request.FILES)  
        if form.is_valid():
            user = form.save(commit=False)
            user.save() 
            auth.authenticate(request=request,kwargs={'user':user})
            auth_login(request, user)
            print request.user
        else:
            return postresult #redirect(reverse("register_phone", kwargs={}))

        return redirect(reverse("home", kwargs={}))

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))