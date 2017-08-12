
用户的扩展要涉及的以下几个方面:
- 用户扩展
- 用户授权

djangoproject - [topics-auth](https://docs.djangoproject.com/en/dev/topics/auth/default)


# django 中的实现
## 数据结构
## 用户授权 authenticate
当项目调用authenticate时，它会直接调用这个函数

django.contrib.auth.__init__

``` python
def authenticate(**credentials):
    """
    If the given credentials are valid, return a User object.
    """
    for backend, backend_path in _get_backends(return_tuples=True):
        try:
            inspect.getcallargs(backend.authenticate, **credentials) # 遍历backend
        except TypeError:
            # This backend doesn't accept these credentials as arguments. Try the next one.
            continue
 
        try:
            user = backend.authenticate(**credentials) # 调用backend的authenticate函数
        except PermissionDenied:
            # This backend says to stop in our tracks - this user should not be allowed in at all.
            return None
        if user is None:
            continue
        # Annotate the user object with the path of the backend.
        user.backend = backend_path
        return user
 
    # The credentials supplied are invalid to all backends, fire signal
    user_login_failed.send(sender=__name__,
            credentials=_clean_credentials(credentials))
```
- (1) inspect.getcallargs(backend.authenticate, **credentials)

首先它会遍历backend，根据参数去找到合适的authenticate函数，这个backend在settings.py文件AUTHENTICATION_BACKENDS里定义。

- (2) user = backend.authenticate(**credentials)

当authenticate函数找到之后，它就会接下来执行授权操作，并返回用户信息

### backend
backend的实现可以参考下面的例子

django.contrib.auth.backends.py
``` python
class ModelBackend(object):
    """
    Authenticates against settings.AUTH_USER_MODEL.
    """
 
    def authenticate(self, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)
        try:
            user = UserModel._default_manager.get_by_natural_key(username)
            if user.check_password(password):
                return user
        except UserModel.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a non-existing user (#20760).
            UserModel().set_password(password)
``` 
如果函数调用authenticate(username, password)或者authenticate(email, password)(如何email是USERNAME_FIELD)，那么该backend会被调用

### 参考文档
[1] https://docs.djangoproject.com/en/dev/topics/auth/customizing/#writing-an-authentication-backend

demo代码里backend的authenticate的参数包含request，调用authenticate时，必须request=request, 
否则django.contrib.auth.__init__的```authenticate(**credentials)```函数在getcallargs这一步会出错，因为request这个参数不能传进```**credentials```

学到这儿的时候对Keyword Arguments理解还不够，刚好学习了一下，可以看一下下面文档
- [Keyword Arguments](https://docs.python.org/2/tutorial/controlflow.html#keyword-arguments)
- [python 中参数*args, **kwargs](http://blog.csdn.net/anhuidelinger/article/details/10011013)

## 登陆 login

__init__.py (site-packages\django\contrib\auth)

``` python
SESSION_KEY = '_auth_user_id'
BACKEND_SESSION_KEY = '_auth_user_backend'
HASH_SESSION_KEY = '_auth_user_hash'
REDIRECT_FIELD_NAME = 'next'
 
def login(request, user):
    """
    Persist a user id and a backend in the request. This way a user doesn't
    have to reauthenticate on every request. Note that data set during
    the anonymous session is retained when the user logs in.
    """
    session_auth_hash = ''
    if user is None:
        user = request.user
    if hasattr(user, 'get_session_auth_hash'):
        session_auth_hash = user.get_session_auth_hash()
 
    if SESSION_KEY in request.session:
        if _get_user_session_key(request) != user.pk or (
                session_auth_hash and
                request.session.get(HASH_SESSION_KEY) != session_auth_hash):
            # To avoid reusing another user's session, create a new, empty
            # session if the existing session corresponds to a different
            # authenticated user.
            request.session.flush()
    else:
        request.session.cycle_key()
 
# 正常用户登录时，会保存这个用户session，这样在response的消息里的request里面会带出去user信息
    request.session[SESSION_KEY] = user._meta.pk.value_to_string(user)
    request.session[BACKEND_SESSION_KEY] = user.backend
    request.session[HASH_SESSION_KEY] = session_auth_hash
    if hasattr(request, 'user'):
        request.user = user
    rotate_token(request)
    user_logged_in.send(sender=user.__class__, request=request, user=user)

```
- (1) request.session[SESSION_KEY]
SESSION_KEY会在后面_get_user_session_key中使用，用于获取用户

注意两个user的差别
``` html
{{user}}
{{request.user}}
 ```
这两个user分别是由下面的middleware传进来的
``` python
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
```

## context_processors
django.contrib.auth.context_processors.auth
``` python
def auth(request):
    """
    Returns context variables required by apps that use Django's authentication
    system.
 
    If there is no 'user' attribute in the request, uses AnonymousUser (from
    django.contrib.auth).
    """
    if hasattr(request, 'user'):
        user = request.user
    else:
        from django.contrib.auth.models import AnonymousUser
        user = AnonymousUser()
 
    return {
        'user': user,
        'perms': PermWrapper(user),
    }
``` 
user赋值在这儿完成，如果是非登陆用户，则为AnonymousUser

## middleware

Middleware.py (site-packages\django\contrib\auth
``` python
def get_user(request):
    if not hasattr(request, '_cached_user'):
        request._cached_user = auth.get_user(request)
return request._cached_user
 
class AuthenticationMiddleware(object):
    def process_request(self, request):
        assert hasattr(request, 'session'), (
            "The Django authentication middleware requires session middleware "
            "to be installed. Edit your MIDDLEWARE_CLASSES setting to insert "
            "'django.contrib.sessions.middleware.SessionMiddleware' before "
            "'django.contrib.auth.middleware.AuthenticationMiddleware'."
        )
        request.user = SimpleLazyObject(lambda: get_user(request))
``` 

## 获取用户 get_user
系统里多个地方都调用了get_user

django/contrib/auth/__init__
``` python
def get_user(request):
    """
    Returns the user model instance associated with the given request session.
    If no user is retrieved an instance of `AnonymousUser` is returned.
    """
    from .models import AnonymousUser
    user = None
    try:
        user_id = _get_user_session_key(request) 
        backend_path = request.session[BACKEND_SESSION_KEY]
    except KeyError:
        pass
    else:
        if backend_path in settings.AUTHENTICATION_BACKENDS:
            backend = load_backend(backend_path)
            user = backend.get_user(user_id)
            # Verify the session
            if ('django.contrib.auth.middleware.SessionAuthenticationMiddleware'
                    in settings.MIDDLEWARE_CLASSES and hasattr(user, 'get_session_auth_hash')):
                session_hash = request.session.get(HASH_SESSION_KEY)
                session_hash_verified = session_hash and constant_time_compare(
                    session_hash,
                    user.get_session_auth_hash()
                )
                if not session_hash_verified:
                    request.session.flush()
                    user = None
 
    return user or AnonymousUser()
```

- (1) _get_user_session_key(request)
SESSION_KEY在login中赋值了

django/contrib/auth/backends.py
``` python
class ModelBackend(object):    
    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            return UserModel._default_manager.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None
```

django/contrib/auth/forms.py
``` python
class AuthenticationForm(forms.Form):
    def get_user(self):
        return self.user_cache
```

django/contrib/auth/middleware.py
``` python
def get_user(request):
    if not hasattr(request, '_cached_user'):
        request._cached_user = auth.get_user(request)
    return request._cached_user
```


## 应用调用
https://docs.djangoproject.com/en/dev/topics/auth/default/#how-to-log-a-user-in
``` python 
from django.contrib.auth import authenticate, login
 
def my_view(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request= request, username=username, password=password)
    if user is not None:
        login(request, user)
        # Redirect to a success page.
        ...
    else:
        # Return an 'invalid login' error message.
        ...
```












