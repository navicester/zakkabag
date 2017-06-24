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
    phone = forms.CharField(label='phone', max_length=18)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    vc = forms.CharField(label='verification code',  max_length=10) 

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        users = UserModel().objects.filter(username=phone)
        if users :
            raise forms.ValidationError('User Exist!')
        return phone

class UserUpdateForm(forms.ModelForm):
    required_css_class = 'required'
    #phone = forms.IntegerField(_('phone'),initial ="+86 000 0000 0000")
    phone = forms.CharField(label='phone', initial ="+86 000 0000 0000")
    birthday = forms.DateField(label='birthday', widget=forms.DateInput, error_messages={'required':'birthday required'})
    #sex = forms.ChoiceField(label='sex', empty_label=None)

    class Meta:
        model = User
        fields = ('username', UsernameField(),'first_name','last_name','sex','birthday','nickname','image') 
        #exclude = ('password',)

