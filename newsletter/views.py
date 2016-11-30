
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from products.models import ProductFeatured,Product
from .forms import SignUpForm,ContactForm
from .models import UserWechat#,SignUp, 
from django.contrib.auth import authenticate#, login, logout
from django.contrib import auth

from django.core.urlresolvers import reverse

from weixin.client import WeixinMpAPI
#from weixin.oauth2 import OAuth2AuthExchangeError
APP_ID = 'wxe90ebbe29377e650'
APP_SECRET = 'd4624c36b6795d1d99dcf0547af5443d'

#from django.contrib.auth.models import User
#http://www.cnblogs.com/smallcoderhujin/p/3193103.html

def home(request):    

    title = 'Sign Up now'
    featured_image = ProductFeatured.objects.filter(active=True).order_by("?").first()
    products = Product.objects.all().order_by("?")[:6]
    products2 = Product.objects.all().order_by("?")[:6]

    # REDIRECT_URI = "http://%s%s" % (request.META['HTTP_HOST'], reverse("home", kwargs={}))

    # try:
    #     code = request.GET.get('code')
    #     if code:
    #         api = WeixinMpAPI(appid=APP_ID, 
    #                     app_secret=APP_SECRET,
    #                     redirect_uri=REDIRECT_URI)
    #         auth_info = api.exchange_code_for_access_token(code=code)
    #         api = WeixinMpAPI(access_token=auth_info['access_token'])
    #         user = api.user(openid=auth_info['openid'])

    #         try:
    #             obj = UserWechat.objects.filter(
    #             openid = user['openid'],
    #             unionid = user['unionid'],
    #             city = user['city'],
    #             country = user['country'],
    #             headimgurl = user['headimgurl'],
    #             language = user['language'],
    #             sex = user['sex'],
    #             privilege = user['privilege'],
    #             nickname = user['nickname']
    #             )[0]
    #         except UserWechat.DoesNotExist:
    #             obj = UserWechat(
    #             openid = user['openid'],
    #             unionid = user['unionid'],
    #             city = user['city'],
    #             country = user['country'],
    #             headimgurl = user['headimgurl'],
    #             language = user['language'],
    #             sex = user['sex'],
    #             privilege = user['privilege'],
    #             nickname = user['nickname']
    #             )
    #             obj.save()

    #         request.session['openid'] = user['openid']
    # except:
    #     pass

    # cuserwechat = None
    # if request.session.get('openid'):
    #     cuserwechat = UserWechat.objects.filter(openid = request.session.get('openid'))[0]

    form = SignUpForm(request.POST or None)
    context = {
        "title": title,
        "form": form,
        "featured_image":featured_image,
        "products":products,
        "products2":products2,
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
    # del request.session['openid']
    try:
        del request.session['wechat_id']
    except:
        pass
    auth.logout(request)
    return redirect(reverse("home", kwargs={}))

def login(request):
    if request.method == 'GET':
        try:
            code = request.GET.get('code')
            if code:
                REDIRECT_URI = "http://%s%s" % (request.META['HTTP_HOST'], reverse("home", kwargs={}))
                user = authenticate(request=request, code=code, app_id=None, app_secret=None, redirect_uri=REDIRECT_URI)
                if user:
                    auth.login(request, user)
                    return redirect(REDIRECT_URI)
                    #return redirect(reverse("home", kwargs={}))
                else:
                    pass
            else:
                pass
        except:
            pass

        return redirect(reverse("auth_login", kwargs={}))
    else:        
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request=request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            # Redirect to a success page.
        else:
            # raise forms.ValidationError(self.error_messages['invalid_login'])
            # Return an 'invalid login' error message.
            pass
    return redirect(reverse("home", kwargs={}))

#from weixin.client import WeixinMpAPI
#from weixin.oauth2 import OAuth2AuthExchangeError
APP_ID = 'wxe90ebbe29377e650'
APP_SECRET = 'd4624c36b6795d1d99dcf0547af5443d'

def wechatlogin(request):
    REDIRECT_URI = "http://%s%s" % (request.META['HTTP_HOST'], reverse("home", kwargs={}))
    api = WeixinMpAPI(appid=APP_ID, app_secret=APP_SECRET,redirect_uri=REDIRECT_URI)
    redirect_uri = api.get_authorize_login_url(scope=("snsapi_userinfo",))
    return redirect(redirect_uri)

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

