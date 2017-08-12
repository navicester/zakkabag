
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
- inspect.getcallargs(backend.authenticate, **credentials)

首先它会遍历backend，根据参数去找到合适的authenticate函数，这个backend在settings.py文件AUTHENTICATION_BACKENDS里定义。

- user = backend.authenticate(**credentials)

当authenticate函数找到之后，它就会接下来执行授权操作，并返回用户信息

demo代码里backend的authenticate的参数包含request，调用authenticate时，必须request=request, 
否则django.contrib.auth.__init__的```authenticate(**credentials)```函数在getcallargs这一步会出错，因为request这个参数不能传进```**credentials```












