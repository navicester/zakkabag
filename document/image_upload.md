
以头像上传为例

# 后台上传

细节可参考ecommerce 017 Image Uploads

https://docs.djangoproject.com/en/1.8/ref/forms/fields/#django.forms.ImageField

在用户里面添加image域，并通过upload_to函数指定保存方法
``` python
def image_upload_to(instance, filename):
    name = instance.username
    title, file_extension = filename.split(".")
    new_filename = "%s-%s.%s" %(instance.id, slugify(title), file_extension)
    return "profile/%s/%s" %(name, new_filename)

class MyUser(AbstractBaseUser, PermissionsMixin):
    image = models.ImageField(upload_to=image_upload_to)
```
media定义
``` python
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, "static_in_env", "media_root")
```
文件上传之后
- 后台Admin显示: 
> 目前: profile/bhe001/1-6-lock.jpg
- 访问网站：
> http://127.0.0.1:8000/media/profile/bhe001/1-6-lock.jpg
- 本地文件保存位置：
> d:\virtualenv\zakkabag\zakkabag\static_in_env\media_root\profile\bhe001\1-6-lock.jpg

同样的名字，如果继续覆盖，文件不会被覆盖，而是增加随机数重新拷贝一个
> 目前: profile/bhe001/1-6-lock_Ni9llB7.jpg 

# 前台上传
首先在personalcenter.templates.personcalcenter.profile_detail.html添加img相关元素

显示组件
``` html
{{form}}
```
显示图片
``` html
<img  id='img' class= 'img-responsive' src="{{object.get_image_url}}"/>
```


在表单中加入```enctype="multipart/form-data；```如果不加则得不到图片信息，只有路径  
FILES是个字典，它包含每个FileField的键 (或者ImageField，FileField的子类)。这样的话就可以用request.FILES['File']来存放表单中的这些数据了。 

注意request.FILES只有在请求方法为POST，并且发送请求的<form>拥有```enctype="multipart/form-data```属性时，才会包含数据。否则request.FILES为空

``` html
{% extends "base.html" %}
{% load crispy_forms_tags %}

{% block content %}

<div class='col-sm-6 col-sm-offset-3'>
	<h3>{{ object }}</h3>
	<form method="POST" enctype="multipart/form-data" action=""> {% csrf_token %}
		{{form|crispy}}
		<img  id='img' class= 'img-responsive' src="{{object.get_image_url}}"/>
		<br>
		<input type="submit" value='Update' class='btn' />
	</form>
</div>

{% endblock %}
```

在personalcenter.views.py 中添加对form的处理
``` python
class ProfileDetailView(FormMixin, DetailView):
    model = UserModel
    template_name = "personalcenter/profile_detail.html"
    form_class = MyUserForm 

    def get_context_data(self, *args, **kwargs):
        context = super(ProfileDetailView, self).get_context_data(*args, **kwargs)
        context["form"] = self.form_class(instance = self.get_object())  
        return context

    def get_object(self, *args, **kwargs):
        user_pk = self.kwargs.get("id")
        usemodel = None
        if user_pk:
            usemodel = get_object_or_404(UserModel, pk=user_pk)
        return usemodel 

    def get_success_url(self):
        return reverse("personalcenter", kwargs=self.kwargs)    

    def post(self, request, *args, **kwargs):
        form = self.get_form()

        if form.is_valid():
            usermodel = UserModel.objects.get(id=self.kwargs.get("id"))
            usermodel.first_name = form.cleaned_data['first_name']
            usermodel.last_name = form.cleaned_data['last_name']

            if 'image' in form.cleaned_data:
                usermodel.image = form.cleaned_data['image'] 
            usermodel.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
```

- form class
``` python
form_class = MyUserForm
```
定义form_class，后面通过通过get_form_class()或get_form()获取form相关的内容

初始化
``` python
context["form"] = self.form_class(instance = self.get_object())
```
Profile是DetailView，本来是不带form的，如果要支持image功能，必须支持form，所以我们添加了基类FormMixin。在form_class指定form类型，并且在context里面将form数据传递给templates。这儿根据object内容对form进行了初始化。

如果是CreateView (例如ProductCreateView)，它的基类有FormMixin，所以form_class是默认已定义的，不需要额外添加FormMixin。不过，如果要添加额外的form，同样需要在context里面传递

更新form内容除了通过instance，也可以直接更新queryset，例如form.fields['categories'].queryset = Category.objects.all()

- get_form()
``` python
form = self.get_form()
```
get_form()会根据定义的form_class获取form类，并根据传递的参数初始化或实例化
在该例子中，我们可以用下面句子代替图片信息获取内容```form = self.form_class(request.POST, request.FILES)``

具体可参考```class FormMixin(six.with_metaclass(FormMixinBase, ContextMixin)):```

``` python
class FormMixin(six.with_metaclass(FormMixinBase, ContextMixin)):
    def get_form_class(self):
        """
        Returns the form class to use in this view
        """
        return self.form_class

    def get_form(self, form_class=None):
        """
        Returns an instance of the form to be used in this view.
        """
        if form_class is None:
            form_class = self.get_form_class()
        return form_class(**self.get_form_kwargs())

    def get_form_kwargs(self):
        """
        Returns the keyword arguments for instantiating the form.
        """
        kwargs = {
            'initial': self.get_initial(),
            'prefix': self.get_prefix(),
        }

        if self.request.method in ('POST', 'PUT'):
            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
            })
        return kwargs
```

- cleaned_data
``` python
usermodel.image = form.cleaned_data['image']
```
该语句获取image对象。也可以通过下面文件处理的方式
``` python
filename=request.FILES['image']
from PIL import Image 
if filename:
    img=Image.open(filename)
img.save(os.path.join(settings.MEDIA_ROOT, photoname))
usermodel.image = photoname
```

效果图如下：

![](img/img_update_personalcenter.png)

# 上传进度条
具体参考：https://github.com/Tonetete/Simple-Django-progressbar-upload-file-form-with-ajax
该文章有相对详细的讲解，但是内容不全
[Upload to Django with progress bar using Ajax and jQuery](http://www.laurentluce.com/posts/upload-to-django-with-progress-bar-using-ajax-and-jquery/)

用到的技术
- [jQuery Form plugin](http://jquery.malsup.com/form/#download)
- ajaxsubmit
- http://malsup.github.io/jquery.form.js
- [jQuery progress bar plugin](http://t.wits.sg/jquery-progress-bar/) 这个当前实现没有，后面可以用这个来代替进度条状态更新的函数
- progressbar
- https://code.jquery.com/ui/1.12.1/jquery-ui.js
- https://code.jquery.com/ui/1.12.1/themes/base/jquery-ui.css
- 文件上传参考函数 https://docs.djangoproject.com/en/1.8/topics/http/file-uploads/








