from django.contrib import admin
# Register your models here.
from .forms import SignUpForm
from .models import SignUp, UserWechat

class SignUpAdmin(admin.ModelAdmin):
	list_display = ["__unicode__", "timestamp", "updated"]
	form = SignUpForm
	# class Meta:
	# 	model = SignUp

class UserWechatAdmin(admin.ModelAdmin):
	list_display = ["openid", "unionid", "nickname"]
	class Meta:
		model = UserWechat
	
admin.site.register(SignUp, SignUpAdmin)
admin.site.register(UserWechat, UserWechatAdmin)
