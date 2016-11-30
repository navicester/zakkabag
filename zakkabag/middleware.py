from django.contrib.auth import get_user_model
from django.utils.functional import SimpleLazyObject

class openidmiddleware():
	def process_response(self, request, response):
		return response


	def process_request(self, request):
		pass
		# wechat_id = request.session.get("wechat_id")
		# if wechat_id:
		# 	UserModel = get_user_model()
		# 	try:
		# 	    #request.user = SimpleLazyObject(UserModel.objects.get(pk=wechat_id))
		# 	    request.user = UserModel.objects.get(pk=wechat_id)
		# 	except  UserModel.DoesNotExist:
		# 		pass