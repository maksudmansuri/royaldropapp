# from django import forms
# from django.contrib.auth.models import User
# from django.contrib.auth.forms import UserCreationForm
# from django.core.exceptions import ValidationError


# class UserRegisterForm(UserCreationForm):
#     first_name = forms.CharField(widget=forms.TextInput(attrs={}))
#     last_name = forms.CharField(widget=forms.TextInput(attrs={}))
#     username = forms.CharField(label=("Mobile Number/Email"),widget=forms.TextInput(attrs={'oninput':'validate()'}))
#     password1 = forms.CharField(label=("Password"), strip=False, widget=forms.PasswordInput(attrs={}),)
#     password2  = forms.CharField(label=("Confirm"), strip=False, widget=forms.PasswordInput(attrs={}),)

#     class Meta:
#         model = User
#         fields = ['username', ]


from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.forms import UserCreationForm
from .models import User


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        class Meta(UserCreationForm.Meta):
             model = User
             fields = ('username',)



    

