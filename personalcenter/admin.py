from django.contrib import admin

# Register your models here.
from .models import MyUser


class MyUserAdmin(admin.ModelAdmin):
	list_display = ["username"]
	class Meta:
		model = MyUser
	
admin.site.register(MyUser, MyUserAdmin)
