from django.conf import settings
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from personalcenter.models import MyUser, WechatUserProfile
from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model
from django.contrib import auth
#from django.core.exceptions import ObjectDoesNotExist

from weixin.client import WeixinMpAPI
#from weixin.oauth2 import OAuth2AuthExchangeError
APP_ID = 'wxe90ebbe29377e650'
APP_SECRET = 'd4624c36b6795d1d99dcf0547af5443d'

#UserModel = 'auth.User' #
#UserModel = settings.AUTH_USER_MODEL
UserModel = get_user_model()

class MyBackend(object):
    
    def authenticate(self, account_type = None, username=None, password=None, **kwargs):        
        user = None
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)
            if username is None:
                return None
        try:
            #user = UserModel.objects.filter(username=username).first()  #fail, why?
            #user = UserModel.objects.get(username=username)  #fail, why?
            user = UserModel._default_manager.get_by_natural_key(username)
            if user.check_password(password):
                return user
        except UserModel.DoesNotExist:
            UserModel().set_password(password)
            return None
        else:
            if user.check_password(password):
                return user
            else:
                return None
 
    def get_user(self, user_id):
        
        try:
            return UserModel._default_manager.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None


class WechatBackend(object):

    def authenticate(self, request, user):

        obj = None
        profile = None

        try:
            profile = WechatUserProfile.objects.get(openid = user['openid'])
            if profile:
                obj = profile.user
            # obj = UserModel._default_manager.get_by_natural_key(user['openid'])
        except WechatUserProfile.DoesNotExist:
            # email = '%s@example.com' % user['openid']
            # password = user['openid']
            # obj = MyUser.objects.create_user(
            #     username = user['openid'],
            #     account_type = 'wechat',
            #     email = email,
            #     password = password,
            #     )
            # obj.is_staff = True

            profile = WechatUserProfile.objects.create(
                user = None, openid = user['openid'])
            profile.unionid = user['unionid']
            #profile.privilege = user['privilege'] #privilege is list
            profile.city = user['city']
            profile.country = user['country']
            profile.language = user['language']
            if 1 == user['sex']:
                profile.sex = 'male'
            else:
                profile.sex = 'female'
            profile.nickname = user['nickname']
            profile.headimgurl = user['headimgurl']
            profile.save()

        request.session['wechat_id'] = profile.id
        # request._cached_user = obj
        request.user = obj
        return obj

    def get_user(self, user_id):
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None

        # if not hasattr(request, '_cached_user'):
        #     request._cached_user = auth.get_user(request)
        # return request._cached_user

class SettingsBackend(object):
    """
    Authenticate against the settings ADMIN_LOGIN and ADMIN_PASSWORD.

    Use the login name and a hash of the password. For example:

    ADMIN_LOGIN = 'admin'
    ADMIN_PASSWORD = 'pbkdf2_sha256$30000$Vo0VlMnkR4Bk$qEvtdyZRWTcOsCnI/oQ7fVOu1XAURIZYoOZ3iq8Dr4M='
    """

    def authenticate(self, request, username=None, password=None):
        login_valid = (settings.ADMIN_LOGIN == username)
        pwd_valid = check_password(password, settings.ADMIN_PASSWORD)
        if login_valid and pwd_valid:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                # Create a new user. There's no need to set a password
                # because only the password from settings.py is checked.
                user = User(username=username)
                user.is_staff = True
                user.is_superuser = True
                user.save()
            return user
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None            