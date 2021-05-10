from django.shortcuts import render , redirect
from .forms import RegisterForm
from django.contrib.auth import login,authenticate,logout
#from django.contrib.auth.models import User
from front.models import Product,Product_Session,ProductCategory,ProductSubCategory,Product_Modules
from math import ceil
from accounts.EmailBackEnd import EmailBackEnd
from django.db.models import Q
from django.core.paginator import Page,PageNotAnInteger,Paginator
from accounts.models import Staffs, Customers as Customers
# Create your vie ws here.v
 
def index(request):
    allProduct=[]
    allcats=[]
    allcrs=Product.objects.all()
    allcrscnt=Product.objects.all().count()
    allstfcnt=Staffs.objects.all().count()
    allstdcnt=Customers.objects.all().count()
    catProduct=Product.objects.values('product_category','id')
    print(catProduct)
    cats={item['product_category'] for item in catProduct}
    for cat in cats:
        allcat=ProductCategory.objects.get(id=cat)
        crs=Product.objects.filter(product_category=cat,is_verified=True)
        n=len(crs)
        # nSlides=n/4+ceil((n/4)-(n//4))    
        allProduct.append([crs,range(1,n)])
        allcats.append(allcat)
        for i in crs:  
            print(i.Product_category)

    print(allcats)
    params= {'allProduct':allProduct,'allcats':allcats,'allcrscnt':allcrscnt,'allstfcnt':allstfcnt,'allstdcnt':allstdcnt,'allcrs':allcrs}
    return render(request,'index.html',params)
    
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

def instructor_logout(request):
    logout(request)
    return redirect('/login')

def about_us(request):
    stf=Staffs.objects.all()
    allcrs=Product.objects.all()
    param={'stf':stf,'allcrs':allcrs}
    return render(request,'about-us.html',param)

def career(request):
    return render(request,'career.html')

def contact_us(request):
    return render(request,'contact-us.html')