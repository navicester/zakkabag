

## 单选改为横向
设置form中的field为 RadioSelect，在template中它会以ul,li方式进行显示
``` python
class OfficeInspectionForm(forms.ModelForm):
      
    plug = forms.MultipleChoiceField(
            choices=RESULT_OPTION,
            widget = forms.RadioSelect,
            )
```
template中显示如下，各个选项(Yes, No0是竖着显示的，排版不够美观，也不符合纸质使用习惯
``` html
<ul id="id_plug">
  <li>
    <label for="id_plug_0"><input checked="checked" id="id_plug_0" name="plug" type="radio" value="yes"> 
      Yes
    </label>
  </li>
  <li>
    <label for="id_plug_1"><input id="id_plug_1" name="plug" type="radio" value="no"> 
      No
    </label>
  </li>
</ul>
```
显示效果如下
![inspection_radioselect_ul_li_raw][img/inspection_radioselect_ul_li_raw.png]

### 隐藏li的默认样式 (去掉圆点)
首选去掉圆点
``` javascript
<style type="text/css">
{% block style %}

.field ul{
	list-style:none;
}

{% endblock%}
</style>
```

### 添加浮动属性
``` javascript

.field li{
	float:left;
}

```

### 参考
[ul li css 做横向菜单](http://www.cnblogs.com/amylis_chen/archive/2011/09/24/2188398.html)

