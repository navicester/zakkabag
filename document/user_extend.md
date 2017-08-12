
用户的扩展要涉及的以下几个方面:
- 用户扩展
- 用户授权

https://docs.djangoproject.com/en/dev/topics/auth/default/#how-to-log-a-user-in


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












