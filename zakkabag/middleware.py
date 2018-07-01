# from django.core.urlresolvers import reverse
# from django.contrib.auth import get_user_model
# from authwrapper.models import WechatUserProfile
from django.conf import settings

# UserModel = get_user_model()

class openidmiddleware():
    def process_response(self, request, response):
#        if request.META['PATH_INFO'] == reverse("auth_login"):
#            account_link_to_wechat(request)
        return response


    def process_request(self, request):
        # request.register_type = settings.ACCOUNT_REGISTER_TYPE
        request.lang = settings.LANGUAGES

        import os
        if settings.USE_SAE_BUCKET: #'SERVER_SOFTWARE' in os.environ:  
            from saewrapper.storage.bucket import SAEBucket
            request.media = SAEBucket().url('')
        else:
            request.media = settings.MEDIA_URL

		# moved to authwrapper middleware                        
        # if request.user.is_anonymous:
        #        from django.utils.module_loading import import_string
        #        backend = import_string('authwrapper.backends.auth.WechatBackend')()
        #        request.wechat = backend.get_wechat_user(request)
