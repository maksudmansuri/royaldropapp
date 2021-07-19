from django.forms import ModelForm
from front.models import Product,ProductChildSubCategory
from accounts.models import Staffs

class ProductCreateView(ModelForm):
    class Meta:
      model=Product
      fields = ["product_desc","product_l_desc"]

class ProductChildSubCategoryCreateVIew(ModelForm):
    class Meta:
      model=ProductChildSubCategory
      fields = ['title','thumbnail','description','is_active']

# class CreateAbout(ModelForm):
#   class Meta:
#     model=Staffs
#     fields = ["about"]


# class CreateSession(ModelForm):
#     class Meta:
#       model=Course_Session
#       fields ='__all__'
    




# from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth import login, authenticate
# from django import forms
# from django.contrib.auth.models import User 

# class RegisterForm(UserCreationForm):
#     email=forms.EmailField()
#   #  DOB=forms.DateField()

#     class Meta:
#         model=User
#         fields =["email","username","password1","password2"]
# class LoginForm(UserCreationForm):

#     class Meta:
#       model=User
#       fields = ['username', 'password']