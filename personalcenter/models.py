from django.db import models
from django.conf import settings
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mail
from django.utils import six, timezone
from django.core import validators
from django.core.urlresolvers import reverse
from django.utils.text import slugify
from django.db.models.signals import pre_save

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

    def create_user(self, username, email=None, password=None, **extra_fields):
        return self._create_user(username, email, password, False, False, **extra_fields)

    def create_superuser(self, **user_data):
        if 'phone' == settings.ACCOUNT_REGISTER_TYPE:
            #{'phone': '13500000000', u'password': '123', 'email': '', 'sex': 'male'}
            #get usename from phone, and unpack the rest
            return self._create_user(user_data['phone'], is_staff=True, is_superuser=True, account_type='phone',
                                 **user_data)
        else:
            return self._create_user(is_staff=True, is_superuser=True, account_type='mail',
                                 **user_data)
    '''
    def create_superuser(self, username, email, password, **extra_fields):
        return self._create_user(username, email, password, True, True,
                                 **extra_fields)
    '''

# register with Phone, email, ....
# for phone register, username will be a repalica of phone number
# for mail register, username and mail is seperated value
USER_TYPE = (
	('username', 'Username'),
	('mail', 'Mail'), 
	('wechat', 'Wechat'),
	('phone', 'Phone'), 
)

SEX_OPTION = (
    ('male', 'Male'),
    ('female', 'Female'),
)

def image_upload_to(instance, filename):
    name = instance.username
    title, file_extension = filename.split(".")
    new_filename = "%s-%s.%s" %(slugify(title), instance.id,  file_extension)
    return "profile/%s/%s" %(name, new_filename)

#Copy from AbstractUser => inherit from AbstractUser directly 
#class AbstractUser(AbstractBaseUser, PermissionsMixin):
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
    phone = models.CharField(_('phone'), max_length=30, blank=True, unique=True,
        help_text=_('Required. digits and + only.'),
        validators=[
            validators.RegexValidator(r'^(130|131|132|133|134|135|136|137|138|139)\d{8}$',
                                      _('Enter a valid phone number. '
                                        'This value may contain only numbers and + characters.'), 'invalid'),
        ],
        error_messages={
            'unique': _("A user with that phone number already exists."),
        })
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    email = models.EmailField(_('email address'), blank=True)
    sex = models.CharField(_('sex'), max_length=30, choices = SEX_OPTION, blank=True, default = 'male')
    birthday = models.DateField(_('birthday'), blank=True, null=True)
    nickname = models.CharField(_('nickname'), max_length=30, blank=True)
    is_staff = models.BooleanField(_('staff status'), default=False,
        help_text=_('Designates whether the user can log into this admin '
                    'site.'))
    is_active = models.BooleanField(_('active'), default=True,
        help_text=_('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
	
    # identifier = models.CharField(max_length=50, unique=True, db_index=True, verbose_name='username')
    account_type = models.CharField(max_length=50, blank=True, null=True, choices=USER_TYPE, default = 'username') #login account type

    image = models.ImageField(upload_to=image_upload_to, blank=True, null=True)

    USERNAME_FIELD = 'phone' if 'phone' == settings.ACCOUNT_REGISTER_TYPE  else 'username'
    REQUIRED_FIELDS = ['mail'] if 'phone' == settings.ACCOUNT_REGISTER_TYPE  else ['phone','email']
 
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
    def is_wechatuser(self):
        try:
            WechatUserProfile.objects.get(user=self)
        except Exception as e:
            return False
        else:
            return True
        finally:
            pass

def myuser_pre_save_receiver(sender, instance, *args, **kwargs):
    if 'phone' == MyUser.USERNAME_FIELD:
        if instance.username is None:
            instance.username = instance.phone

pre_save.connect(myuser_pre_save_receiver, sender=MyUser)

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

class UserProfile(models.Model): 
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    score = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    # score_available = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    # score_frozen = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    # score_owned = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    # score_spent = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    level = models.DecimalField(max_digits=10, decimal_places=0, default=0)

    def __unicode__(self):  
        return str(self.user)
