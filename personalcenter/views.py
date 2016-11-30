from django.shortcuts import render, get_object_or_404
from newsletter.models import UserWechat

from django.contrib.auth import get_user_model
UserModel = get_user_model()

# Create your views here.
def personalcenterhome(request,id):

    wechatuser = get_object_or_404(UserModel, id=id)
    try:
        wechatuser = UserModel.objects.get(id=id)
    except UserModel.DoesNotExist:
        raise Http404
    except:
        raise Http404

    template = "personalcenter/personalcenterhome.html"
    context = {    
        "object": wechatuser
    }

    return render(request, template, context)