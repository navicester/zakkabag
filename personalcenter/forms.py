from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import MyUser

class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = MyUser
        fields = ('email', 'phone')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

#refer to django/contrib/auth/forms.py
class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = MyUser
        fields = '__all__' #('email', 'password', 'first_name', 'last_name', 'is_active', 'is_staff', 'account_type')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]

class MyUserForm(forms.ModelForm):
    class Meta:
        model = MyUser

        fields = [
            'first_name',
            'last_name',
            'image',
        ]
        

    def clean_image(self):
        if self.cleaned_data.get("image") != None:
            return self.cleaned_data.get("image")
        elif self.data.get("image") == None:    
            raise forms.ValidationError("image can't be empty.")
        else:
            self.cleaned_data['image'] = self.data.get("image")
            return self.data.get("image")

    def is_valid(self):
        if self.clean_image != None:
            return True
        return False        