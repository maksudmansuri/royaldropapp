from django.contrib import admin
from .models import Product,ProductCategory,ProductSubCategory,Product_Session,Product_Modules

admin.site.register(Product)
admin.site.register(ProductCategory)
admin.site.register(ProductSubCategory)
admin.site.register(Product_Session)
admin.site.register(Product_Modules)
