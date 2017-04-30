
from django.conf import settings
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from products.models import ProductFeatured,Product
from django.shortcuts import render, redirect
from .forms import SignUpForm,ContactForm
from .models import UserWechat,Banner, Article
from django.contrib import auth
from django.contrib.auth import authenticate#, login, logout
from django.contrib.auth import views as auth_views
from zakkabag.settings import APP_ID, APP_SECRET


from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView, CreateView
from django.core.urlresolvers import reverse
# from django.contrib.auth.forms import AuthenticationForm
# from django.utils.http import is_safe_url
# from django.http import HttpResponseRedirect


from weixin.client import WeixinMpAPI
#from weixin.oauth2 import OAuth2AuthExchangeError

#from django.contrib.auth.models import User
#http://www.cnblogs.com/smallcoderhujin/p/3193103.html

def home(request):    

    title = 'Sign Up now'
    featured_image = ProductFeatured.objects.filter(active=True).order_by("?").first()
    featured_images = ProductFeatured.objects.all()
    products = Product.objects.all().order_by("?")[:6]
    products2 = Product.objects.all().order_by("?")[:6]
    banners = Banner.objects.filter(active=True).order_by("?")[:6]

    form = SignUpForm(request.POST or None)
    context = {
        "title": title,
        "form": form,
        "featured_image":featured_image,
        'featured_images':featured_images,
        "products":products,
        "products2":products2,
        'banners':banners,
        # 'userwechat': cuserwechat,

    }
    
    if form.is_valid():
        #form.save()
        #print request.POST['email'] #not recommended, raw data without validation
        instance = form.save(commit=False)

        full_name = form.cleaned_data.get("full_name")
        if not full_name:
            full_name = "New full name"
        instance.full_name = full_name
        # if not instance.full_name:
        #     instance.full_name = "Justin"
        instance.save()
        context = {
            "title": "Thank you"
        }

    return render(request, "home.html", context)

def logout(request):
    try:
        del request.session['wechat_id']
    except:
        pass
    auth.logout(request)
    return redirect(reverse("home", kwargs={}))

#refer to django/contrib/auth/views.py
#http://127.0.0.1:8000/accounts/activate/??
def login(request):
    REDIRECT_URI = request.POST.get('next', request.GET.get('next', reverse("home", kwargs={}))) #next indicated in templaetes
    if request.method == 'GET':
        print '44444444444'
        code = request.GET.get('code')
        if code:
            print '1111111111111'
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
                print '222222222222'
                auth.login(request, user)
                return redirect(redirect_to)

        return redirect(reverse("auth_login", kwargs={}))
    else:  #normal login is POST
        print '33333333'
        REDIRECT_FIELD_NAME = 'next'
        return auth_views.login(request, redirect_field_name=REDIRECT_FIELD_NAME, extra_context=None)    

        # below method is also OK
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request=request, username=username, password=password)
        if user is not None:
            auth.login(request, user)                
        else:
            return redirect(reverse("auth_login", kwargs={}))

    return auth_views.login(request, redirect_field_name=REDIRECT_URI, extra_context=None)    

def contact(request):
    title = 'Contact Us'    
    title_align_center = True
    form = ContactForm(request.POST or None)

    if form.is_valid():
        # for key, value in form.cleaned_data.iteritems():
        #     print key, value
        #     #print form.cleaned_data.get(key)

        form_email = form.cleaned_data.get("email")
        form_message = form.cleaned_data.get("message")
        form_full_name = form.cleaned_data.get("full_name")
        # print email, message, full_name
        subject = 'Site contact form'
        from_email = settings.EMAIL_HOST_USER
        to_email = [from_email, form_email]

        contact_message = "%s: %s via %s"%( 
                form_full_name, 
                form_message, 
                form_email)
        some_html_message = """
        <h1>hello</h1>
        """

        # import smtplib
        # try:
        #     smtpObj = smtplib.SMTP() 
        #     smtpObj.connect(settings.EMAIL_HOST, 25)
        #     smtpObj.login(settings.EMAIL_HOST_USER,settings.EMAIL_HOST_PASSWORD)  
        #     smtpObj.sendmail(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_USER, some_html_message)
        #     print "sent successfully !!!!!!!!!!!!!!!!"
        # except smtplib.SMTPException:
        #     print "Error: sent fail $$$$$$$$$$$$$$"

        send_mail(subject, 
                contact_message, 
                from_email, 
                to_email, 
                html_message=some_html_message,
                fail_silently=False)

    context = {
        "form": form,
        "title": title,
        "title_align_center": title_align_center,
    }
    return render(request, "forms.html", context)

class ArticleDetailView(DetailView):
    model = Article
    template_name = "article/article_detail.html"
    def get_context_data(self, *args, **kwargs):
        context = super(ArticleDetailView, self).get_context_data(*args, **kwargs)
        context["object"] = self.get_object()
        return context        

    def get(self, request, *args, **kwargs):
        return super(ArticleDetailView, self).get(request, *args, **kwargs) 

    def dispatch(self, request, *args, **kwargs):
        instance = self.get_object()
        request.breadcrumbs([
            ("Home",reverse("home", kwargs={})),
            ("Newsletter",reverse("ArticleListView", kwargs={})),
            (instance.title,request.path_info),
        ])
        return super(ArticleDetailView, self).dispatch(request,args,kwargs)      

class ArticleListView(ListView): 
    model = Article
    template_name = "article/article_list.html"

    def get_context_data(self, *args, **kwargs):
        context = super(ArticleListView, self).get_context_data(*args, **kwargs)
        context["objects"] = Article.objects.all()
        return context       

    def dispatch(self, request, *args, **kwargs):
        request.breadcrumbs([
            ("Home",reverse("home", kwargs={})),
            ('Newsletter',request.path_info),
        ])
        return super(ArticleListView, self).dispatch(request,args,kwargs)   



