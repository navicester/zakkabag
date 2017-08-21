import os
from django.conf import settings

#DEBUG = False
#TEMPLATE_DEBUG = False

DATABASES = settings.DATABASES

MYSQL_HOST = 'w.rdc.sae.sina.com.cn'
MYSQL_PORT = '3307'
MYSQL_USER = 'lno2o5x0ox' #ACCESSKEY
MYSQL_PASS = 'jx3531ximhkk5z5h3l4myx41w330x3lyz0zz1x3m' #SECRETKEY
MYSQL_DB   = 'app_zakkabag'


MYSQL_HOST = 'mclkvoqfrfqv.mysql.sae.sina.com.cn'
MYSQL_PORT = '10099'
MYSQL_USER = 'bhe001'
MYSQL_PASS = 'majia101214'
MYSQL_DB   = 'szakkabag'

if not 'SERVER_SOFTWARE' in os.environ:
	import sae
	from sae._restful_mysql import monkey
	monkey.patch()

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