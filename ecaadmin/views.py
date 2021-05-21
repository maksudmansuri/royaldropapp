from django.contrib.messages import views
from django.http.response import HttpResponse
from django.shortcuts import render
from django.views.generic import ListView,CreateView,UpdateView,DetailView,View
from front.models import Product, ProductSubCategory,ProductCategory,productMedia,ProductQuestions,ProductReviews,ProductVarient,ProductAbout,ProductComments,ProductDetails,ProductReviewVoting,ProductTag,ProductTransaction,ProductVariantItems
from django.contrib.messages.views import SuccessMessageMixin
from accounts.models import CustomUser, Customers, Merchants, Staffs
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.db.models import Q
from .form import ProductCreateView
from eca.settings import BASE_URL
from django.views.decorators.csrf import csrf_exempt
# Create your views here.


def admin_home(request):
    return render(request,"ecaadmin/home.html")

class ProductCategoryListViews(ListView):
    model=ProductCategory
    template_name="ecaadmin/category_list.html"
    paginate_by=3

    def get_queryset(self):
        filter_val=self.request.GET.get("filter","")
        order_by=self.request.GET.get("orderby","id")
        if filter_val!="":
            cat=ProductCategory.objects.filter(Q(title__contains=filter_val) | Q(description__contains=filter_val)).order_by(order_by)
        else:
            cat=ProductCategory.objects.all().order_by(order_by)

        return cat
   
    def get_context_data(self,**kwargs):
        context=super(ProductCategoryListViews,self).get_context_data(**kwargs)
        context["filter"]=self.request.GET.get("filter","")
        context["orderby"]=self.request.GET.get("orderby","id")
        context["all_table_fields"]=ProductCategory._meta.get_fields()
        return context
        
class ProductCategoryUpdate(SuccessMessageMixin,UpdateView):
    model = ProductCategory
    success_message = "category Updated!"
    fields = ['title','thumbnail','description','is_active']
    print(fields)
    template_name = "ecaadmin/category_update.html"

class ProductCategoryCreate(SuccessMessageMixin,CreateView):
    model = ProductCategory
    success_message = "category added"
    fields = ['title','thumbnail','description','is_active']
    template_name = "ecaadmin/category_create.html"

class ProductSubCategoryListViews(ListView):
    model = ProductSubCategory
    template_name = "ecaadmin/subcategory_list.html"
    paginate_by=3

    def get_queryset(self):
        filter_val=self.request.GET.get("filter","")
        order_by=self.request.GET.get("orderby","id")
        if filter_val!="":
            cat=ProductSubCategory.objects.filter(Q(title__contains=filter_val) | Q(description__contains=filter_val)).order_by(order_by)
        else:
            cat=ProductSubCategory.objects.all().order_by(order_by)

        return cat
   
    def get_context_data(self,**kwargs):
        context=super(ProductSubCategoryListViews,self).get_context_data(**kwargs)
        context["filter"]=self.request.GET.get("filter","")
        context["orderby"]=self.request.GET.get("orderby","id")
        context["all_table_fields"]=ProductSubCategory._meta.get_fields()
        return context

class ProductSubCategoryUpdate(SuccessMessageMixin,UpdateView):
    model = ProductSubCategory
    success_message = "category Updated!"
    fields = ['category','title','thumbnail','description','is_active']
    template_name = "ecaadmin/subcategory_update.html"

class ProductSubCategoryCreate(SuccessMessageMixin,CreateView):
    model = ProductSubCategory
    success_message = "subcategory added"
    fields = ['category','title','thumbnail','description','is_active']
    template_name = "ecaadmin/subcategory_create.html"

class MerchantUserCreateView(SuccessMessageMixin,CreateView):
    model = CustomUser
    success_message = "Merchant added !"
    template_name = "ecaadmin/merchant_create.html"
    fields = ['first_name','last_name','email','phone','username','password']

    def form_valid(self, form):
        # user = form.save(commit=False) this will not not WORK WITH auto intense
        username=self.request.POST.get("username")
        password=self.request.POST.get("password")
        email=self.request.POST.get("email")
        print(username,password,email)
        user=CustomUser.objects.create_user(username=username,password=password,email=email,user_type=4)
        user.is_active=True
        # user.user_type = "2"
        # user.set_password(form.cleaned_data["password"])
        user.phone=self.request.POST.get("phone")
        user.first_name=self.request.POST.get("first_name")
        user.last_name=self.request.POST.get("last_name")

        user.save()

        profile_pic=self.request.FILES['profile_pic']
        fs=FileSystemStorage()
        filename=fs.save(profile_pic.name,profile_pic)
        profile_pic_url = fs.url(filename)

        # print(profile_pic_url)

        # print(user.merchants)
        # merchant = Merchants.objects.get(admin=user.id)
        # print(merchant)
        user.merchants.profile_pic=profile_pic_url
        user.merchants.company_name=self.request.POST.get("company_name")
        user.merchants.gts_number=self.request.POST.get("gts_number")
        user.merchants.address=self.request.POST.get("address")

        is_added_by_admin = False

        if self.request.POST.get("is_added_by_admin") == "on":
            is_added_by_admin=True
        user.merchants.is_added_by_admin=is_added_by_admin
        user.save()

        messages.success(self.request,"Merchant Created Succesfully")
        return HttpResponseRedirect(reverse("merchant_list"))
          
class MerchantUserUpdate(SuccessMessageMixin,UpdateView):
    model = CustomUser
    success_message = "Merchant updated !"
    template_name = "ecaadmin/merchant_update.html"
    fields = ['first_name','last_name','email','phone','username','password']

    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        merchant =Merchants.objects.get(admin_id=self.object.pk)
        context["merchant"] = merchant
        return context

    def form_valid(self, form):
        user = form.save(commit=False) #this will not not WORK WITH auto intense
        user.save()

        merchant  = Merchants.objects.get(admin_id=user.id)
        if self.request.FILES.get('profile_pic'):
            profile_pic=self.request.FILES['profile_pic']
            fs=FileSystemStorage()
            filename=fs.save(profile_pic.name,profile_pic)
            profile_pic_url = fs.url(filename)
            merchant.profile_pic=profile_pic_url

        merchant.company_name=self.request.POST.get("company_name")
        merchant.gts_number=self.request.POST.get("gts_number")
        merchant.address=self.request.POST.get("address")

        is_added_by_admin = False

        if self.request.POST.get("is_added_by_admin") == "on":
            is_added_by_admin=True
        merchant.is_added_by_admin=is_added_by_admin
        merchant.save()

        messages.success(self.request,"Merchant Created Succesfully")
        return HttpResponseRedirect(reverse("merchant_list"))

class MerchantUserListViews(ListView):
    model = Merchants
    template_name = "ecaadmin/merchant_list.html"
   
class ProductListViews(ListView):
    model = Product
    template_name = "ecaadmin/product_list.html"
    paginate_by=3

    def get_queryset(self):
        filter_val=self.request.GET.get("filter","")
        order_by=self.request.GET.get("orderby","id")
        if filter_val!="":
            products=Product.objects.filter(Q(product_name__contains=filter_val) | Q(product_desc__contains=filter_val)).order_by(order_by)
        else:
            products=Product.objects.all().order_by(order_by)
        product_list=[]
        for product in products:
            product_media=productMedia.objects.filter(product=product.id,media_type=1,is_active=1).first()
            product_list.append({"product":product,"media":product_media})
        
        return product_list
   
    def get_context_data(self,**kwargs):
        context=super(ProductListViews,self).get_context_data(**kwargs)
        context["filter"]=self.request.GET.get("filter","")
        context["orderby"]=self.request.GET.get("orderby","id")
        context["all_table_fields"]=Product._meta.get_fields()
        return context

class ProductUpdate(View):
    
    def get(self,request,*args,**kwargs):
        product_id=kwargs["product_id"]
        product=Product.objects.get(id=product_id)
        product_details=ProductDetails.objects.filter(product=product_id)
        product_about=ProductAbout.objects.filter(product=product_id)
        product_tag=ProductTag.objects.filter(product=product_id)

        categories = ProductCategory.objects.filter(is_active=1)
        categories_list = []
        for category in categories:
            sub_category = ProductSubCategory.objects.filter(is_active=1,category_id=category.id)
            categories_list.append({"category":category,"sub_category":sub_category})     

        return render(request,"ecaadmin/product_update.html",{"categories":categories_list,"product":product,"product_details":product_details,"product_about":product_about,"product_tag":product_tag})

    def post(self,request,*args,**kwargs):

        product_name=request.POST.get("product_name")
        product_brand=request.POST.get("product_brand")
        product_model_number=request.POST.get("product_model_number")
        sub_category=request.POST.get("sub_category")
        product_mrp=request.POST.get("product_mrp")
        product_selling_price=request.POST.get("product_selling_price")
        product_desc=request.POST.get("product_desc")
        product_weight=request.POST.get("product_weight")
        details_ids=request.POST.getlist("details_id[]")
        title_title_list=request.POST.getlist("title_title[]")
        about_ids=request.POST.getlist("about_id[]")
        title_details_list=request.POST.getlist("title_details[]")
        about_title_list=request.POST.getlist("about_title[]")
        product_tags=request.POST.get("product_tags")
        long_desc=request.POST.get("long_desc")

        subcat_obj=ProductSubCategory.objects.get(id=sub_category)
        
        product_id=kwargs["product_id"]
        product=Product.objects.get(id=product_id)
        product.product_name=product_name
        product.product_brand=product_brand
        product.product_model_number=product_model_number
        product.product_subcategory=subcat_obj
        product.product_mrp=product_mrp
        product.product_selling_price=product_selling_price
        product.product_weight=product_weight 
        product.product_desc=product_desc
        product.product_l_desc=long_desc
               
        product.save()

        j=0
        for title_title in title_title_list:
            detail_id=details_ids[j]
            if detail_id == "blank" and title_title != "":
                product_details=ProductDetails(title=title_title,title_details=title_details_list[j],product=product)
                product_details.save()                
            else:
                if title_title != "":
                    product_details=ProductDetails.objects.get(id=detail_id)
                    product_details.title=title_title
                    product_details.title_details=title_details_list[j]
                    product_details.product=product
                    product_details.save()
            j=j+1

        k=0
        for about in about_title_list:
            about_id=about_ids[k]
            if about_id == "blank" and about != "":
                product_about=ProductAbout(title=about,product=product)
                product_about.save()
            else:
                if about != "":
                    product_about=ProductAbout.objects.get(id=about_id)
                    product_about.title=about
                    product_about.product=product
                    product_about.save()
            k=k+1

        ProductTag.objects.filter(product=product_id).delete()

        product_tags_list=product_tags.split(",")

        for product_tag in product_tags_list:
            product_tag_obj=ProductTag(product_tags=product_tag,product=product)
            product_tag_obj.save()

        return HttpResponse("ok")
    

class ProductView(View):
    def get(self,request,*args,**kwargs):
        form=ProductCreateView()
        categories = ProductCategory.objects.filter(is_active=1)
        categories_list = []
        for category in categories:
            sub_category = ProductSubCategory.objects.filter(is_active=1,category_id=category.id)
            categories_list.append({"category":category,"sub_category":sub_category})
        merchants_users=Merchants.objects.filter(admin_id__is_active =True)
        return render(self.request,"ecaadmin/product_create.html",{"categories":categories_list,'merchants_users':merchants_users,'form':form})
    
    def post(self,request,*args,**kwargs):
        product_name=request.POST.get("product_name")
        product_brand=request.POST.get("product_brand")
        product_model_number=request.POST.get("product_model_number")
        sub_category=request.POST.get("sub_category")
        product_mrp=request.POST.get("product_mrp")
        product_selling_price=request.POST.get("product_selling_price")
        product_desc=request.POST.get("product_desc")
        product_weight=request.POST.get("product_weight")
        added_by_merchant=request.POST.get("added_by_merchant")
        in_stock_total=request.POST.get("in_stock_total")
        media_type_list=request.POST.getlist("media_type[]")
        media_content_list=request.FILES.getlist("media_content[]")
        title_title_list=request.POST.getlist("title_title[]")
        title_details_list=request.POST.getlist("title_details[]")
        about_title_list=request.POST.getlist("about_title[]")
        product_tags=request.POST.get("product_tags")
        long_desc=request.POST.get("long_desc")

        subcat_obj=ProductSubCategory.objects.get(id=sub_category)
        merchant_user_obj=Merchants.objects.get(id=added_by_merchant)

        product=Product(product_name=product_name,product_brand=product_brand,product_model_number=product_model_number,product_subcategory=subcat_obj,product_mrp=product_mrp,product_selling_price=product_selling_price,product_weight=product_weight,product_desc=product_desc,product_l_desc=long_desc,in_stock_total=in_stock_total,added_by_merchant=merchant_user_obj)
        
        product.save()

        i=0
        for media_content in media_content_list:
            fs=FileSystemStorage()
            filename=fs.save(media_content.name,media_content)
            media_url=fs.url(filename)
            product_media = productMedia(product=product,media_type=media_type_list[i],media_content=media_url)
            product_media.save()
            i=i+1

        j=0
        for title_title in title_title_list:
            product_details=ProductDetails(title=title_title,title_details=title_details_list[j],product=product)
            product_details.save()
            j=j+1
        k=0
        for about in about_title_list:
            product_about=ProductAbout(title=about,product=product)
            product_about.save()
            k=k+1

        product_tags_list=product_tags.split(",")

        for product_tag in product_tags_list:
            product_tag_obj=ProductTag(product_tags=product_tag,product=product)
            product_tag_obj.save()

        product_transaction=ProductTransaction(product=product,transation_type=1,transation_product_count=in_stock_total,transation_desc="initial item added in stock")
        product_transaction.save()
        return HttpResponse("ok")

@csrf_exempt
def file_upload(request):
    file=request.FILES["file"]
    fs=FileSystemStorage()
    filename=fs.save(file.name,file)
    file_url=fs.url(filename)
    return HttpResponse('{"location":"'+BASE_URL+''+file_url+'"}')

class ProductAddMedia(View):
    def get(self,request,*args, **kwargs):
        product_id=kwargs["product_id"]
        product=Product.objects.get(id=product_id)
        return render(request,"ecaadmin/product_add_media.html",{"product":product})

    def post(self,request,*args, **kwargs):
        product_id=kwargs["product_id"]
        product=Product.objects.get(id=product_id)
        media_type_list=request.POST.getlist("media_type[]")
        media_content_list=request.FILES.getlist("media_content[]")

        i=0
        for media_content in media_content_list:
            fs=FileSystemStorage()
            filename=fs.save(media_content.name,media_content)
            media_url=fs.url(filename)
            product_media = productMedia(product=product,media_type=media_type_list[i],media_content=media_url)
            product_media.save()
            i=i+1
        return HttpResponse("ok")




class ProductEditMedia(View):
    def get(self,request,*args,**kwargs):
        product_id=kwargs["product_id"]
        product=Product.objects.get(id=product_id)
        product_medias=productMedia.objects.filter(product=product_id)
        return render(request,"ecaadmin/product_edit_media.html",{"product":product,"product_medias":product_medias})

class ProductMediaDelete(View):
    def get(self,request,*args,**kwargs):
        media_id=kwargs["id"]
        product_media=productMedia.objects.get(id=media_id)
        import os
        from eca import settings

        #It will work too Sometimes
        #product_media.media_content.delete()
        os.remove(settings.MEDIA_ROOT.replace("\media","")+str(product_media.media_content).replace("/","\\"))
        
        product_id=product_media.product.id
        product_media.delete()
        return HttpResponseRedirect(reverse("product_edit_media",kwargs={"product_id":product_id}))

class ProductAddStocks(View):
    def get(self,request,*args,**kwargs):
        product_id=kwargs["product_id"]
        product=Product.objects.get(id=product_id)
        return render(request,"ecaadmin/product_add_stocks.html",{"product":product})

    def post(self,request,*args,**kwargs):
        product_id=kwargs["product_id"]
        new_instock=request.POST.get("add_stocks")
        product=Product.objects.get(id=product_id)
        old_stocks=product.in_stock_total
        new_stocks=int(new_instock)+int(old_stocks)
        product.in_stock_total=new_stocks
        product.save()

        product_obj=Product.objects.get(id=product_id)
        product_transaction=ProductTransaction(product=product_obj,transaction_product_count=new_instock,transaction_description="New Product Added",transaction_type=1)
        product_transaction.save()
        return HttpResponseRedirect(reverse("product_add_stocks",kwargs={"product_id":product_id}))


class StaffUserListView(ListView):
    model=Staffs
    template_name="ecaadmin/staff_list.html"
    paginate_by=3

    def get_queryset(self):
        filter_val=self.request.GET.get("filter","")
        order_by=self.request.GET.get("orderby","id")
        if filter_val!="":
            cat=Staffs.objects.filter(Q(admin_id__first_name__contains=filter_val) |Q(admin_id__last_name__contains=filter_val) | Q(admin_id__email__contains=filter_val) | Q(admin_id__username__contains=filter_val) | Q(admin_id__phone__contains=filter_val)).order_by(order_by)
        else:
            cat=Staffs.objects.all().order_by(order_by)

        return cat

    def get_context_data(self,**kwargs):
        context=super(StaffUserListView,self).get_context_data(**kwargs)
        context["filter"]=self.request.GET.get("filter","")
        context["orderby"]=self.request.GET.get("orderby","id")
        context["all_table_fields"]=Staffs._meta.get_fields()
        return context


class StaffUserCreateView(SuccessMessageMixin,CreateView):
    template_name="ecaadmin/staff_create.html"
    model=CustomUser
    fields=["first_name","last_name","email","phone","username","password"]

    def form_valid(self,form):

        #Saving Custom User Object for Merchant User
        user=form.save(commit=False)
        user.is_active=True
        user.user_type=2
        user.set_password(form.cleaned_data["password"])
        user.save()

        #Saving Merchant user
        profile_pic=self.request.FILES["profile_pic"]
        fs=FileSystemStorage()
        filename=fs.save(profile_pic.name,profile_pic)
        profile_pic_url=fs.url(filename)

        user.staffuser.profile_pic=profile_pic_url
        user.save()
        messages.success(self.request,"Staff User Created")
        return HttpResponseRedirect(reverse("staff_list"))

class StaffUserUpdateView(SuccessMessageMixin,UpdateView):
    template_name="ecaadmin/staff_update.html"
    model=CustomUser
    fields=["first_name","last_name","email","phone","username",]

    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        staffuser=Staffs.objects.get(admin_id=self.object.pk)
        context["staffuser"]=staffuser
        return context

    def form_valid(self,form):

        #Saving Custom User Object for Merchant User
        user=form.save(commit=False)
        user.save()

        #Saving Merchant user
        staffuser=Staffs.objects.get(admin_id=user.id)
        if self.request.FILES.get("profile_pic",False):
            profile_pic=self.request.FILES["profile_pic"]
            fs=FileSystemStorage()
            filename=fs.save(profile_pic.name,profile_pic)
            profile_pic_url=fs.url(filename)
            staffuser.profile_pic=profile_pic_url

        staffuser.save()
        messages.success(self.request,"Staff User Updated")
        return HttpResponseRedirect(reverse("staff_list"))


class CustomerUserListView(ListView):
    model=Customers
    template_name="ecaadmin/customer_list.html"
    paginate_by=3

    def get_queryset(self):
        filter_val=self.request.GET.get("filter","")
        order_by=self.request.GET.get("orderby","id")
        if filter_val!="":
            cat=Customers.objects.filter(Q(admin_id__first_name__contains=filter_val) |Q(admin_id__last_name__contains=filter_val) | Q(admin_id__email__contains=filter_val) | Q(admin_id__username__contains=filter_val)).order_by(order_by)
        else:
            cat=Customers.objects.all().order_by(order_by)

        return cat

    def get_context_data(self,**kwargs):
        context=super(CustomerUserListView,self).get_context_data(**kwargs)
        context["filter"]=self.request.GET.get("filter","")
        context["orderby"]=self.request.GET.get("orderby","id")
        context["all_table_fields"]=Customers._meta.get_fields()
        return context


class CustomerUserCreateView(SuccessMessageMixin,CreateView):
    template_name="ecaadmin/customer_create.html"
    model=CustomUser
    fields=["first_name","last_name","email","phone","username","password"]

    def form_valid(self,form):

        #Saving Custom User Object for Merchant User
        user=form.save(commit=False)
        user.is_active=True
        user.user_type=3
        user.set_password(form.cleaned_data["password"])
        user.save()

        #Saving Merchant user
        profile_pic=self.request.FILES["profile_pic"]
        fs=FileSystemStorage()
        filename=fs.save(profile_pic.name,profile_pic)
        profile_pic_url=fs.url(filename)

        user.customers.profile_pic=profile_pic_url
        user.save()
        messages.success(self.request,"Customer User Created")
        return HttpResponseRedirect(reverse("customer_list"))

class CustomerUserUpdateView(SuccessMessageMixin,UpdateView):
    template_name="ecaadmin/customer_update.html"
    model=CustomUser
    fields=["first_name","last_name","email","phone","username"]

    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        customeruser=Customers.objects.get(admin_id=self.object.pk)
        context["CustomerUser"]=customeruser
        return context

    def form_valid(self,form):

        #Saving Custom User Object for Merchant User
        user=form.save(commit=False)
        user.save()

        #Saving Merchant user
        customeruser=Customers.objects.get(admin_id=user.id)
        if self.request.FILES.get("profile_pic",False):
            profile_pic=self.request.FILES["profile_pic"]
            fs=FileSystemStorage()
            filename=fs.save(profile_pic.name,profile_pic)
            profile_pic_url=fs.url(filename)
            customeruser.profile_pic=profile_pic_url

        customeruser.save()
        messages.success(self.request,"Customer User Updated")
        return HttpResponseRedirect(reverse("customer_list"))