 # -*- coding: utf-8 -*-

"""
Django settings for zakkabag project.

Generated by 'django-admin startproject' using Django 1.8.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

#BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) #add settings as dedicated folder

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'u(+p48v^a25q!d6lrc3oou)_%v%xwj^xc*)5f_t=(iefi278m('

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

ADMINS = (
    ('countrysidedog', 'csdog@countrysidedog.com'),
)

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'django_comments',   
    # 'django.contrib.comments',
    'authwrapper',
    'mptt',
    'comments',
    'newsletter',
    'products',
    'carts',
    'orders',
    'personalcenter',
    'crowdfundings',
    'inspection',
    'zakkabag',
    'crispy_forms',
    'registration',
    'django_filters',
    # 'threadedcomments',
    'pagination',
    'ckeditor',
    'phone_login',
    'rest_framework'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',    
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'zakkabag.middleware.openidmiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',    
    'pagination.middleware.PaginationMiddleware',
    'breadcrumbs.middleware.BreadcrumbsMiddleware',
)

ROOT_URLCONF = 'zakkabag.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "templates"), 
                os.path.join(BASE_DIR, "comments","templates"),
                os.path.join(BASE_DIR, "authwrapper","templates"),
                os.path.join(BASE_DIR, "wechat","templates"),
                os.path.join(BASE_DIR, "fileuploadwrapper","templates"),
                os.path.join(BASE_DIR, "crowdfundings")],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                "django.core.context_processors.i18n",
                "zakkabag.templatecontext.lang_context_processor",
            ],
        },
    },
]


WSGI_APPLICATION = 'zakkabag.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

if not 'SERVER_SOFTWARE' in os.environ: 
	DATABASES = {
		'default': {
			'ENGINE': 'django.db.backends.sqlite3',
			'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
		}
	}



# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en' #'en-us', language switch fail

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


LANGUAGES_SUPPORTED = ('en', 'zh-cn',)

LANGUAGES = (
    ('en', ('English')),
    ('zh-cn', ('中文简体')),
    ('zh-tw', ('中文繁體')),
)


'''
#from django.utils.translation import ugettext as _

ugettext = lambda s: s

LANGUAGES = (
    ('en-us', ugettext('English')),
    ('zh-cn', ugettext('Chinese Simple')),
    ('zh-tw', ugettext('Chinese taiwan')),
)
'''

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'
# STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), "static_in_env", "static_root")
STATIC_ROOT = os.path.join(BASE_DIR, "static_in_env", "static_root")

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static_in_pro", "our_static"),
    #os.path.join(BASE_DIR, "static_in_env"),
    #'/var/www/static/',
)

if 'SERVER_SOFTWARE' in os.environ:    
    FILE_UPLOAD_MAX_MEMORY_SIZE = 10485760 # 10M
    DEFAULT_FILE_STORAGE = 'sae.ext.django.storage.backend.Storage'
    #DEFAULT_FILE_STORAGE = 'saewrapper.storage.SAEStorage'
    STORAGE_BUCKET_NAME = 'media'
    # ref: https://docs.djangoproject.com/en/dev/topics/files/
    '''
    STORAGE_ACCOUNT = 'zakkabag'
    STORAGE_ACCESSKEY = 'lno2o5x0ox'
    STORAGE_SECRETKEY = 'jx3531ximhkk5z5h3l4myx41w330x3lyz0zz1x3m'
    os.environ.setdefault("sae.storage.path", os.path.join(BASE_DIR, "static_in_env2"))
    '''

    CKEDITOR_UPLOAD_PATH = 'ckeditor/uploads' #not valid
else:
    MEDIA_ROOT = os.path.join(BASE_DIR, "static_in_env", "media_root")
    CKEDITOR_UPLOAD_PATH = os.path.join(MEDIA_ROOT, 'ckeditor/uploads') #not used

MEDIA_URL = '/media/'

#print "base dir" + BASE_DIR
#print "STATIC_ROOT" + STATIC_ROOT
#print STATICFILES_DIRS

try:
    import settings_security
    EMAIL_HOST_USER = settings_security.USER_NAME
    EMAIL_HOST_PASSWORD = settings_security.USER_PWD
    DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
except:
    EMAIL_HOST_USER = ''
    EMAIL_HOST_PASSWORD = ''
    DEFAULT_FROM_EMAIL = ''

EMAIL_HOST = 'smtp.sina.com'
EMAIL_PORT = 25
EMAIL_USE_TLS = True

#SERVER_EMAIL = DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

'''
EMAIL_HOST = 'smtp.sina.com'
EMAIL_PORT = 25

EMAIL_HOST = 'smtp.163.com'
EMAIL_PORT = 465

EMAIL_HOST = 'smtp.exmail.qq.com'
EMAIL_PORT = 465
'''




#Crispy FORM TAGs SETTINGS
CRISPY_TEMPLATE_PACK = 'bootstrap3'

#DJANGO REGISTRATION REDUX SETTINGS
ACCOUNT_ACTIVATION_DAYS = 7
REGISTRATION_AUTO_LOGIN = True
SITE_ID = 1

LOGIN_REDIRECT_URL = '/'
REGISTRATION_EMAIL_SUBJECT_PREFIX = '[Django Registration zakkabag]'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
#EMAIL_BACKEND = 'sae.ext.django.mail.backend.EmailBackend'
SEND_ACTIVATION_EMAIL = True

AUTHENTICATION_BACKENDS = (    
    
    'authwrapper.backends.auth.WechatBackend',
    'authwrapper.backends.auth.MyBackend',       
    'django.contrib.auth.backends.ModelBackend', 
    )
AUTH_USER_MODEL = 'authwrapper.MyUser'

# COMMENTS_APP = 'threadedcomments'
COMMENTS_APP = 'comments'


from django.conf import global_settings
FILE_UPLOAD_HANDLERS = ('fileuploadwrapper.uploadfilehandler.UploadProgressCachedHandler', ) \
+ global_settings.FILE_UPLOAD_HANDLERS


# Wechat
if not 'SERVER_SOFTWARE' in os.environ:
    APP_ID = 'wxe90ebbe29377e650' #changyubingfeng
    APP_SECRET = 'd4624c36b6795d1d99dcf0547af5443d'    
else:
    APP_ID = 'wx168434ba37e8c17b' #
    APP_SECRET = 'd4624c36b6795d1d99dcf0547af5443d'

ACCOUNT_REGISTER_TYPE = 'phone' #phone, mail
ACCOUNT_ALLOW_MIX_TYPE_LOGIN = True

PHONE_LOGIN_ATTEMPTS = 100

USE_EXPLICIT_LANG_URL = False

