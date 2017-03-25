from django.db import models
from django.conf import settings
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mail
from django.utils import six, timezone
from django.core import validators
from django.core.urlresolvers import reverse
from django.utils.text import slugify

# Create your models here.

class MyUserManager(BaseUserManager): 
    use_in_migrations = True

    def _create_user(self, username, email, password,
                     is_staff, is_superuser, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        now = timezone.now()
        if not username:
            raise ValueError('The given username must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email,
                          is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, account_type='mail',email=None, password=None, **extra_fields):
        if 'wechat' == account_type:
            return self._create_user(username, email, password, False, False,
                                     **extra_fields)
        else:
            return self._create_user(username, email, password, False, False,
                                     **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        return self._create_user(username, email, password, True, True,
                                 **extra_fields)

USER_TYPE = (
	('username', 'Username'),
	('mail', 'Mail'),
	('wechat', 'Wechat'),
	('phone', 'Phone'),
)

def image_upload_to(instance, filename):
    name = instance.username
    title, file_extension = filename.split(".")
    new_filename = "%s-%s.%s" %(instance.id, slugify(title), file_extension)
    return "profile/%s/%s" %(name, new_filename)

#Copy from AbstractUser
class MyUser(AbstractBaseUser, PermissionsMixin):
#class MyUser(AbstractUser): 
    """
    An abstract base class implementing a fully featured User model with
    admin-compliant permissions.

    Username, password and email are required. Other fields are optional.
    """
    username = models.CharField(_('username'), max_length=30, unique=True,
        help_text=_('Required. 30 characters or fewer. Letters, digits and '
                    '@/./+/-/_ only.'),
        validators=[
            validators.RegexValidator(r'^[\w.@+-]+$',
                                      _('Enter a valid username. '
                                        'This value may contain only letters, numbers '
                                        'and @/./+/-/_ characters.'), 'invalid'),
        ],
        error_messages={
            'unique': _("A user with that username already exists."),
        })
    phone = models.CharField(_('phone'), max_length=30, blank=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    email = models.EmailField(_('email address'), blank=True)
    is_staff = models.BooleanField(_('staff status'), default=False,
        help_text=_('Designates whether the user can log into this admin '
                    'site.'))
    is_active = models.BooleanField(_('active'), default=True,
        help_text=_('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
	
    # identifier = models.CharField(max_length=50, unique=True, db_index=True, verbose_name='username')
    account_type = models.CharField(max_length=50, blank=True, null=True, choices=USER_TYPE, default = 'username')

    image = models.ImageField(upload_to=image_upload_to)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
 
    objects = MyUserManager()
 
    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()
 
    def get_short_name(self):
        "Returns the short name for the user."
        return self.first_name
 
    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def __unicode__(self):
        return self.username
 
    def has_perm(self, perm, obj=None):
        return super(MyUser, self).has_perm(perm, obj)
 
    def has_module_perms(self, app_label):
        return super(MyUser, self).has_module_perms(app_label)

    def get_wechatprofile(self):
    	if self.account_type == 'wechat':
    		return WechatUserProfile.objects.get(user__id = self.id)
    	else:
    		return None
    def get_absolute_url(self):
        return reverse("personalcenter", kwargs={"id": self.id })  

    def get_image_url(self):
        if self.image:
            return self.image.url
        else:
            return '/media/profile/bhe001/bhe001-1.jpg'

class WechatUserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank = True,
        null = True
    )
    openid = models.CharField(max_length=120, blank=True, null=True) #wechat only
    unionid = models.CharField(max_length=120, blank=True, null=True) #wechat only
    privilege = models.CharField(max_length=120, blank=True, null=True) #wechat only    
    headimgurl = models.CharField(max_length=500, blank=True, null=True)
    nickname = models.CharField(max_length=120, blank=True, null=True)
    sex = models.CharField(max_length=45, blank=True, null=True)	
    city = models.CharField(max_length=45, blank=True, null=True)
    country = models.CharField(max_length=45, blank=True, null=True)	
    language = models.CharField(max_length=45, blank=True, null=True)

    def __unicode__(self):
        if self.nickname:
        	return self.nickname
        elif self.user:
        	return self.user.username
        else:
        	return self.openid

    def get_absolute_url(self):
        return reverse("personalcenter", kwargs={"id": self.id })  

    def get_image_url(self):
        return self.headimgurl #None        

# class UserProfile(models.Model): 
#     user = models.OneToOneField(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.CASCADE,
#     )

#     score = models.DecimalField(max_digits=10, decimal_places=0, default=100)
#     level = models.DecimalField(max_digits=10, decimal_places=0, default=0)

#     def __unicode__(self):  
#         return user
