from django.contrib import admin

# Register your models here.
from .models import MyUser, UserProfile
from .forms import UserCreationForm, UserChangeForm
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group


class UserProfileAdmin(admin.ModelAdmin):
	list_display = ["user","score","level"]
	class Meta:
		model = UserProfile

#refer to django/contrib/auth/admin.py
class UserAdmin(BaseUserAdmin):
    ''' 
    The forms to add and change user instances
    '''
    form = UserChangeForm
    add_form = UserCreationForm

    '''
    The fields to be used in displaying the User model.
    These override the definitions on the base UserAdmin
    that reference specific fields on auth.User.
    '''

    list_display = ('username', 'phone','email', 'sex','birthday','nickname','is_staff')
    list_filter = ('account_type','is_staff',)
    fieldsets = (
        (None, 
        	{'fields': 
        	('username','phone','email', 'password')}),
        ('Personal info', 
        	{'fields': ('first_name','last_name', 'sex','birthday','nickname','account_type','image')}),
        ('Permissions', 
        	{'fields': ('is_staff','is_active', 'is_superuser','groups', 'user_permissions')}),
        ('Important dates', 
            {'fields': ('last_login', 'date_joined')}),
    )
    
    '''
    add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    overrides get_fieldsets to use this attribute when creating a user.
    '''
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username','phone', 'email', 'password1', 'password2')}
        ),
    )
    search_fields = ('phone','email',)
    ordering = ('email',)
    filter_horizontal = ()

# Now register the new UserAdmin...
admin.site.register(MyUser, UserAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
#admin.site.unregister(Group)

