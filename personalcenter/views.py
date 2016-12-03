from django.shortcuts import render, get_object_or_404
from django.contrib import auth
from .models import WechatUserProfile
from orders.models import Order
from products.models import Product
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.views.generic.detail import DetailView

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


class ProfileDetailView(DetailView):
    model = UserModel
    template_name = "personalcenter/profile_detail.html"

    def get_context_data(self, *args, **kwargs):
        context = super(ProfileDetailView, self).get_context_data(*args, **kwargs)
        obj = self.get_object()
        # product_set = obj.product_set.all()
        # default_products = obj.default_category.all()
        # products = ( product_set | default_products ).distinct()
        # context["products"] = products
        # context["categories"] = Category.objects.all()
        return context