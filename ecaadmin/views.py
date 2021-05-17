from django.shortcuts import render
from django.views.generic import ListView,CreateView,UpdateView,DetailView
from front.models import ProductSubCategory,ProductCategory
from django.contrib.messages.views import SuccessMessageMixin
# Create your views here.


def admin_home(request):
    return render(request,"ecaadmin/home.html")

 
class ProductCategoryListViews(ListView):
    model = ProductCategory
    template_name = "ecaadmin/category_list.html"


class ProductCategoryUpdate(SuccessMessageMixin,UpdateView):
    model = ProductCategory
    success_message = "category Updated!"
    fields = "__all__"
    print(fields)
    template_name = "ecaadmin/category_update.html"

class ProductCategoryCreate(SuccessMessageMixin,CreateView):
    model = ProductCategory
    success_message = "category added"
    fields = "__all__"
    template_name = "ecaadmin/category_create.html"


