from django.shortcuts import render, get_object_or_404
from newsletter.models import UserWechat

# Create your views here.
def personalcenterhome(request,id):

    wechatuser = get_object_or_404(UserWechat, id=id)
    try:
        wechatuser = UserWechat.objects.get(id=id)
    except UserWechat.DoesNotExist:
        raise Http404
    except:
        raise Http404

    template = "personalcenter/personalcenterhome.html"
    context = {    
        "object": wechatuser
    }

    return render(request, template, context)