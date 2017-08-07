# 安装
python qrcode需要用到PIL和qrcode库，首先安装这些库

```
pip install qrcode
pip install image
```

pypi： https://pypi.python.org/pypi/qrcode

# 二维码生成
## 简单用法
``` python
import qrcode
img = qrcode.make('some data here')
img.save('somedatahere.jpg')
img.show()
```

## 高级用法
``` python
import qrcode
qr=qrcode.QRCode(
     version = 2,
     error_correction = qrcode.constants.ERROR_CORRECT_L,
     box_size=10,
     border=10,)
qr.add_data('http://zakkabag.applinzi.com/newsletter/')
qr.make(fit=True)
img = qr.make_image()
img.show()
#img.save('test.jpg')
```
**参数解释**
> The **version** parameter is an integer from 1 to 40 that controls the size of the QR Code (the smallest, version 1, is a 21x21 matrix). 
> Set to None and use the **fit** parameter when making the code to determine this automatically.
>
> The **error_correction** parameter controls the error correction used for the QR Code. The following four constants are made available on the qrcode package:
>
> ERROR_CORRECT_L  
> About 7% or less errors can be corrected.  
> ERROR_CORRECT_M (default)  
> About 15% or less errors can be corrected.  
> ERROR_CORRECT_Q  
> About 25% or less errors can be corrected.  
> ERROR_CORRECT_H.  
> About 30% or less errors can be corrected.
>
> The **box_size** parameter controls how many pixels each “box” of the QR code is.
>
> The **border** parameter controls how many boxes thick the border should be (the default is 4, which is the minimum according to the specs).

## 生成带图案的二维码
接着上面的基本用法
``` python
import qrcode
qr=qrcode.QRCode(
     version = 2,
     error_correction = qrcode.constants.ERROR_CORRECT_L,
     box_size=10,
     border=10,)
qr.add_data('http://zakkabag.applinzi.com/newsletter/')
qr.make(fit=True)
img = qr.make_image()
```





