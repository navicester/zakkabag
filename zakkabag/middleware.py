from django.contrib.auth import get_user_model
from personalcenter.models import WechatUserProfile
UserModel = get_user_model()

class openidmiddleware():
	def process_response(self, request, response):
		return response


	def process_request(self, request):
		if request.user.is_anonymous:
			wechat_id = request.session.get("wechat_id")
			if wechat_id:
				try:
					request.wechat = WechatUserProfile.objects.get(pk=wechat_id)
				except:
					pass
				'''
				try:
				    request.user = UserModel.objects.get(pk=wechat_id)				    
				except  UserModel.DoesNotExist:
					pass
				'''