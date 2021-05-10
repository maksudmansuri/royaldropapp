from django.contrib import admin
# from .models import Account
from accounts.models import CustomUser,AdminHOD
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
# from .forms import UserCreationForm, UserChangeForm
# from .forms import RegistrationsForm

# class UserModel(UserAdmin): 
#     list_display=('email','username','user_type')
#     search_fields = ('email','username')
  
# class ProductAdmin(admin.ModelAdmin):
    #  fieldsets = [
#         ("Product basic Details",{"fields": ["product_code","product_name","product_category","product_subcategory","product_fee","product_duration"]}),
#         ("Product Details",{"fields": ["product_image","product_video","product_level","product_slug","product_ratting","product_pub_date"]}),
#         ("Product Desc",{"fields": ["product_requirement","product_desc","product_why_take","product_syllabus","product_in_pdf"]})

# class CustomUserAdmin(UserAdmin):
#     CustomUser=get_user_model()
class CustomUserAdmin(UserAdmin):
    # form = UserChangeForm
    # add_form = UserCreationForm
    list_display=('email','username')
    search_fields = ('email','username',)
    list_filter = ('is_superuser',)
    filter_horizontal = ()
    # list_filter = ()
    fieldsets = [
        ("Product basic Details",{"fields": ["product_code","product_name","product_category","product_subcategory","product_fee","product_duration"]}),
        ("Product Details",{"fields": ["product_image","product_video","product_level","product_slug","product_ratting","product_pub_date"]}),
        ("Product Desc",{"fields": ["product_requirement","product_desc","product_why_take","product_syllabus","product_in_pdf"]})

    ]

admin.site.register(CustomUser,CustomUserAdmin)


# admin.site.register(CustomUser)
# admin.site.register(AdminHOD)