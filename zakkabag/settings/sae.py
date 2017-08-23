import os
from django.conf import settings
import settings_security

#DEBUG = False
#TEMPLATE_DEBUG = False

DATABASES = settings.DATABASES

#exclusive database
MYSQL_HOST = 'mclkvoqfrfqv.mysql.sae.sina.com.cn'
MYSQL_PORT = '10099'
MYSQL_USER = settings_security.MYSQL_USER
MYSQL_PASS = settings_security.MYSQL_PASS
MYSQL_DB   = 'szakkabag'

# shared database
MYSQL_HOST = 'w.rdc.sae.sina.com.cn'
MYSQL_PORT = '3307'
MYSQL_USER = 'lno2o5x0ox' #ACCESSKEY
MYSQL_PASS = 'jx3531ximhkk5z5h3l4myx41w330x3lyz0zz1x3m' #SECRETKEY
MYSQL_DB   = 'app_zakkabag'

'''
if not 'SERVER_SOFTWARE' in os.environ:
	import sae
	from sae._restful_mysql import monkey
	monkey.patch()
'''

DATABASES = {
    'default': {
        'ENGINE':   'django.db.backends.mysql',
        'NAME':     MYSQL_DB,
        'USER':     MYSQL_USER,
        'PASSWORD': MYSQL_PASS,
        'HOST':     MYSQL_HOST,
        'PORT':     MYSQL_PORT,
    }
}