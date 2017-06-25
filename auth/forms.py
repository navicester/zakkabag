from django import forms

from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import UserCreationForm

from .users import UserModel, UsernameField
User = UserModel()

'''
from django.core.validators import RegexValidator
from django.forms import fields
from django.forms.fields import MultiValueField, CharField
class PhoneField(MultiValueField):
    def __init__(self, *args, **kwargs):
        # Define one message for all fields.
        error_messages = {
            'incomplete': 'Enter a country calling code and a phone number.',
        }
        # Or define a different message for each field.
        fields = (
            CharField(
                error_messages={'incomplete': 'Enter a country calling code.'},
                validators=[
                    RegexValidator(r'^[0-9]+$', 'Enter a valid country calling code.'),
                ],
            ),
            CharField(
                error_messages={'incomplete': 'Enter a phone number.'},
                validators=[RegexValidator(r'^[0-9]+$', 'Enter a valid phone number.')],
            ),
            CharField(
                validators=[RegexValidator(r'^[0-9]+$', 'Enter a valid extension.')],
                required=False,
            ),
        )
        super(PhoneField, self).__init__(
            error_messages=error_messages, fields=fields,
            require_all_fields=False, *args, **kwargs
        )



         
'''

class RegistrationForm(forms.Form):
    """docstring for PhoneRegisterForm"forms.formf __init__(self, arg):
        super(PhoneRegisterForm,forms.form.__init__()
        self.arg = arg
    """
    phone = forms.CharField(label='Phone', max_length=18)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    vc = forms.CharField(label='Verification Code',  max_length=10) 

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        users = UserModel().objects.filter(phone=phone)
        if users :
            raise forms.ValidationError('User Exist!')
            return phone
        import re 
        pattern = re.compile(r'^(130|131|132|133|134|135|136|137|138|139)\d{8}$') 
        match = pattern.search(phone) 
        if not match:
            raise forms.ValidationError('Please input valid phone number !')
        return phone

from django.forms.extras.widgets import SelectDateWidget
from django.contrib.admin import widgets

class UserUpdateForm(forms.ModelForm):
    required_css_class = 'required'
    phone = forms.CharField(label='phone')
    #birthday = forms.DateField(label='birthday', widget=SelectDateWidget, error_messages={'required':'birthday required'})
    birthday = forms.DateField(label='birthday', 
        #widget=forms.DateInput(attrs={'cols': 10, 'rows': 50, 'readonly':'readonly','disable':True}),  #WORK
        #widget=SelectDateWidget(),
        widget=widgets.AdminDateWidget(),
        error_messages={'required':'birthday required'})
    #sex = forms.ChoiceField(label='sex', empty_label=None)


    #can specify widget or widget attribute in init function
    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        self.fields['birthday'].widget = widgets.AdminDateWidget()
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.fields['phone'].widget.attrs['readonly'] = True


    ''' NOT WORK
    widgets = {
        'phone': forms.CharField(attrs={'cols': 10, 'rows': 50, 'readonly':'readonly','disable':True}),
    }
    '''

    def clean_phone():
        instance = getattr(self, 'instance', None)
        if instance and instance.id:
            return instance.phone
        else:
            return self.cleaned_data['phone']

    class Meta:
        model = User
        fields = (UsernameField(),'first_name','last_name','sex','birthday','nickname','image') 
        #fields = ('first_name','last_name','sex','birthday','nickname','image') 
        #exclude = ('password',)

