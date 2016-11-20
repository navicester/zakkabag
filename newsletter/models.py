from django.db import models
from django.conf import settings

# Create your models here.
class SignUp(models.Model):
	email = models.EmailField()
	full_name = models.CharField(max_length=120, blank=True, null=True)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
	updated = models.DateTimeField(auto_now_add=False, auto_now=True)

	def __unicode__(self): #Python 3.3 is __str__
		return self.email

class UserWechat(models.Model):
	#user = models.OneToOneField(settings.AUTH_USER_MODEL, null=True, blank=True) #not required
	openid = models.CharField(max_length=120, blank=True, null=True)
	unionid = models.CharField(max_length=120, blank=True, null=True)
	city = models.CharField(max_length=120, blank=True, null=True)
	country = models.CharField(max_length=120, blank=True, null=True)	
	headimgurl = models.CharField(max_length=120, blank=True, null=True)
	language = models.CharField(max_length=120, blank=True, null=True)
	sex = models.CharField(max_length=120, blank=True, null=True)	
	privilege = models.CharField(max_length=120, blank=True, null=True)
	nickname = models.CharField(max_length=120, blank=True, null=True)

	def __unicode__(self): #def __str__(self):
		return self.nickname

	def admin_user_id(self):
		if self.user:
			return str(self.user.id)
		else:
			return "None" 