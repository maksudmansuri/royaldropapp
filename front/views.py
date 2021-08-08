from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import models
from django.shortcuts import get_object_or_404, render , redirect
# from django.views.generic.base import View
from .forms import RegisterForm
from django.contrib.auth import login,authenticate,logout
#from django.contrib.auth.models import User
from front.models import Product, ProductChildSubCategory, ProductDetails,Product_Session,ProductCategory,ProductSubCategory,Product_Modules, productMedia
from math import ceil
from accounts.EmailBackEnd import EmailBackEnd
from django.db.models import Q, fields
from django.core.paginator import Page,PageNotAnInteger,Paginator
from accounts.models import CustomersAddress, Staffs, Customers as Customers
from django.views.generic import ListView,CreateView,UpdateView,DetailView,View
from django import template
from django.urls import reverse
from django.contrib import messages
from django.http.response import HttpResponse, HttpResponseRedirect

register = template.Library()
# Create your vie ws here.v
 
#use it for url and its section inside same page
@register.simple_tag
def anchor(url_name, section_id):
    return reverse(url_name) + '#' + section_id

# class CategoriesListViews(ListView):
#     model = ProductCategory
#     tem_name = "front/category_list.html"

# class CategoriesCreateView(CreateView):
#     model = ProductCategory
#     fields = "__all__"
#     template_name = "front/categorycreate.html"

class indexView(ListView):
    model = Product
    fields ="__all__"
    template_name="index.html"
 
    def get(self,request,*args,**kwargs):
        product_list = []
        products=Product.objects.filter(is_active=1)
        n=len(products)
        nSlides=n//4 + ceil((n/4)-(n//4))
        params={'no_of_slides':nSlides,'range':range(nSlides),'product':products}
        productcategory = ProductCategory.objects.filter(is_active=1)
        productsubcategory = ProductSubCategory.objects.filter(is_active=1)
        for product in products:
            media=productMedia.objects.filter(product=product).first()
            product_list.append({"product":product,"media":media})
        return render(request,"index.html",{"productcategory":productcategory,"productsubcategory":productsubcategory,"products":product_list})
    
# def index(request):
    # allProduct=[]
    # allcats=[]
    # allcrs=Product.objects.all()
    # allcrscnt=Product.objects.all().count()
    # allstfcnt=Staffs.objects.all().count()
    # allstdcnt=Customers.objects.all().count()
    # catProduct=Product.objects.values('product_category','id')
    # print(catProduct)
    # cats={item['product_category'] for item in catProduct}
    # for cat in cats:
    #     allcat=ProductCategory.objects.get(id=cat)
    #     crs=Product.objects.filter(product_category=cat,is_verified=True)
    #     n=len(crs)
    #     # nSlides=n/4+ceil((n/4)-(n//4))    
    #     allProduct.append([crs,range(1,n)])
    #     allcats.append(allcat)
    #     for i in crs:  
    #         print(i.Product_category)

    # print(allcats)
    # params= {'allProduct':allProduct,'allcats':allcats,'allcrscnt':allcrscnt,'allstfcnt':allstfcnt,'allstdcnt':allstdcnt,'allcrs':allcrs}
    # return render(request,'index.html')
 
class HomeListview(ListView):
    model = Product
    fields ="__all__"
    template_name="index2.html"
     
    def get_queryset(self):
        filter_val=self.request.GET.get("filter","")
        order_by=self.request.GET.get("orderby","id")
        if filter_val!="":
            product=Product.objects.filter(Q(product_name__contains=filter_val) | Q(product_brand__contains=filter_val) | Q(product_desc__contains=filter_val) | Q(product_l_desc__contains=filter_val) |Q(updated_at__contains=filter_val) ).order_by(order_by)
        else:
            product=Product.objects.all().order_by(order_by)

        return product
   
    def get_context_data(self,**kwargs):
        context=super(HomeListview,self).get_context_data(**kwargs)
        context["filter"]=self.request.GET.get("filter","")
        context["orderby"]=self.request.GET.get("orderby","id")
        context["all_table_fields"]=Product._meta.get_fields()
        return context
 
    def get(self,request,*args,**kwargs):
        caties = ProductCategory.objects.filter(is_active=True)
        subcaties = ProductSubCategory.objects.filter(is_active=True)
        
        allprods=[]
        catprods=Product.objects.values('product_category')
        subcatprod=Product.objects.values('product_subcategory')
        # print(subcatprods)
        # print(catprods)
        subcatprods = {item['product_subcategory'] for item in subcatprod}
        cats={item['product_category'] for item in catprods}
        prod =[]
        for cat in cats:
            prods = Product.objects.filter(product_category=cat,is_active=1)
            # print(prods)
            prod =[]
            for product in prods: 
                media=productMedia.objects.filter(product=product).first()
                prod.append({"product":product,"media":media})            
            n=len(prod)
            # print(prod)
            nSlides=n//4 + ceil((n/4)-(n//4))
            productcategories = ProductCategory.objects.get(id=cat,is_active=1)
            # productsubcategories=[]
            # for productcategory in productcategories:
            #     productsubcategy = ProductSubCategory.objects.filter(category=productcategory,is_active=1)
            #     productsubcategories.append({productsubcategy})
            
            prodsub=ProductSubCategory.objects.filter(category=cat,is_active=1)
            allprods.append([prod,range(nSlides),nSlides,productcategories,prodsub])           
        print(allprods)
        params={'allprods':allprods,"cats":caties,"subcaties":subcaties}
        return render(request,"index2.html",params)

class CartListView(ListView): 
    def get(self, request, *args, **kwargs):
        product = Product.objects.filter(is_active=True)
        customer = Customers.objects.get(admin=request.user.id)
        param = {"product":product,"customer":customer}
        return render(request,"cart.html",param)
 
class ProductFilterListView(ListView):

    def get(self, request, *args, **kwargs):
        caties = ProductCategory.objects.filter(is_active=True)
        subCaties = ProductSubCategory.objects.filter(is_active=True)
        childSubCaties = ProductChildSubCategory.objects.filter(is_active=True)
        products = Product.objects.filter(is_active=True)        

        categories = ProductCategory.objects.filter(is_active=1)
        categories_list = []
        for category in categories:
            print(category)
            sub_categories = ProductSubCategory.objects.filter(is_active=1,category=category)
            subcategories_list = []
            print(sub_categories)
            for sub_category in sub_categories:
                print(sub_category)
                childsubcategies = ProductChildSubCategory.objects.filter(is_active=1,subcategory=sub_category)
                print(childsubcategies)
                subcategories_list.append({"sub_category":sub_category,"childsubcategies":childsubcategies})
            categories_list.append({"category":category,"subcategories_list":subcategories_list})
        params={'categories':categories_list,"cats":caties,"subcaties":subCaties,"product_list":products}
        return render(request,"product_filter_list.html",params)


    # def get(self,request,*args,**kwargs):
    #     caties = ProductCategory.objects.filter(is_active=True)
    #     subcaties = ProductSubCategory.objects.filter(is_active=True)
    #     products=Product.objects.filter(is_active=True)

        
    #     allprods=[]
    #     catprods=Product.objects.values('product_category')
    #     subcatprod=Product.objects.values('product_subcategory')
    #     # print(subcatprods)
    #     # print(catprods)
    #     subcatprods = {item['product_subcategory'] for item in subcatprod}
    #     cats={item['product_category'] for item in catprods}
    #     prod =[]
    #     for cat in cats:
    #         prods = Product.objects.filter(product_category=cat,is_active=1)
    #         # print(prods)
    #         prod =[]
    #         for product in prods: 
    #             media=productMedia.objects.filter(product=product).first()
    #             prod.append({"product":product,"media":media})            
    #         n=len(prod)
    #         # print(prod)
    #         nSlides=n//4 + ceil((n/4)-(n//4))
    #         productcategories = ProductCategory.objects.get(id=cat,is_active=1)
    #         # productsubcategories=[]
    #         # for productcategory in productcategories:
    #         #     productsubcategy = ProductSubCategory.objects.filter(category=productcategory,is_active=1)
    #         #     productsubcategories.append({productsubcategy})
            
    #         prodsub=ProductSubCategory.objects.filter(category=cat,is_active=1)
    #         allprods.append([prod,range(nSlides),nSlides,productcategories,prodsub])           
    #     # print(allprods)
    #     print(products)
    #     params={'allprods':allprods,"cats":caties,"subcaties":subcaties}
    #     return render(request,"product_filter_list.html",{'products_list':products})

def home_two(request):
    return render(request,'home_two.html')

def search_list(query=None):
    queryset = []
    queries = query.split(" ")
    for q in queries:
        Products = Product.objects.filter(
            (Q(Product_name__icontains = q) | Q(Product_desc__icontains = q)) & Q(is_verified=True) 
            ).distinct()

        for Product in Products:
            queryset.append(Product)
    
    return list(set(queryset)) 
 

class baseView(ListView):
    def get(self, request, *args, **kwargs):
        related_products = Product.objects.filter(is_active=1)
        catProduct=Product.objects.values('Product_category','id')
        cats={item['Product_category'] for item in catProduct}
        allcats=[]
        for cat in cats:
            allcat=ProductCategory.objects.get(id=cat)
            # crs=Product.objects.filter(Product_category=cat,is_verified=True)
            crscnt=Product.objects.filter(Product_category=cat).count()
            # nSlides=n/4+ceil((n/4)-(n//4))
            # Products.append(crs)
            allcats.append([allcat,crscnt])
        context = {'related_products':related_products}
        return render(request, 'product_detail.html', context)

class ProductDetailView(DetailView): 
    def get(self, request, *args, **kwargs):
        product = get_object_or_404(Product, product_slug=kwargs['product_slug'])
        related_products = Product.objects.filter(product_category=product.product_category,is_active=1)         
        media = productMedia.objects.filter(product=product)
        abouts = ProductDetails.objects.filter(product=product)
        context = {'product': product,'media':media,'abouts':abouts,'related_products':related_products}
        print(related_products)
        return render(request, 'product_detail.html', context)
    
def Product_list(request):
    stf=Staffs.objects.all()
    allcrs=Product.objects.all()
    Products=[]
    allcats=[]
    catProduct=Product.objects.values('Product_category','id')
    cats={item['Product_category'] for item in catProduct}
    for cat in cats:
        allcat=ProductCategory.objects.get(id=cat)
        # crs=Product.objects.filter(Product_category=cat,is_verified=True)
        crscnt=Product.objects.filter(Product_category=cat).count()
        # nSlides=n/4+ceil((n/4)-(n//4))
        # Products.append(crs)
        allcats.append([allcat,crscnt])

    Products=Product.objects.filter(is_verified=True)
    cnt=Product.objects.filter().count()
    # allcat=ProductCategory.objects.all()
    allsubcat=ProductSubCategory.objects.all()
    paginator=Paginator(Products,6)
    page=request.GET.get('page')
    Products=paginator.get_page(page)
    param={'allcat':allcats,'allsubcat':allsubcat,'Products1':Products,'cnt':cnt,'stf':stf,'allcrs':allcrs}
    return render(request,'Product_list.html',param)

def testing_file(request):
    allProduct=[]
    catProduct=Product.objects.values('Product_category','Product_code')
    cats={item['Product_category'] for item in catProduct}
    for cat in cats:
        crs=Product.objects.filter(Product_category=cat)
        n=len(crs)
        nSlides=n/4+ceil((n/4)-(n//4))    
        allProduct.append([crs,range(1,n),nSlides])
    # Products=Product.objects.all()
    # print(Products)
    # n=len(Products)
    # nSlides=n/3+ceil((n/4)-(n//4))
    #  params= {'no_of_slides':n, 'range':range(0,n), 'Product':Products}
    # print(params)
    params= {'allProduct':allProduct}
    print(crs)
    
    return render(request,'testing_file.html',params)
 
def Product_details(request,slug):
    stf=Staffs.objects.all()
    allcrs=Product.objects.all()
    crs=Product.objects.get(Product_slug=slug)
    crs_ssn=Product_Modules.objects.filter(Product=crs)
    # crs_ssn=Product_Session.objects.filter(module.Product_id==mdl.Product)
    print(crs_ssn)
    crssame=Product.objects.filter(Product_category=crs.Product_category)
    # crssame=Product.objects.all()
    params= {'crs1':crs,'crs_ssn1':crs_ssn,'crssame1':crssame,'stf':stf,'allcrs':allcrs}
    return render(request,'Product_details.html',params)

def Product_details_2(request):
    return render(request,'Product_details_2.html')

def dologout(request):
    logout(request)
    return redirect('/')

def about_us(request):
    stf=Staffs.objects.all()
    allcrs=Product.objects.all()
    param={'stf':stf,'allcrs':allcrs}
    return render(request,'about-us.html',param)

def career(request):
    return render(request,'career.html')

def contact_us(request):
    return render(request,'contact-us.html')