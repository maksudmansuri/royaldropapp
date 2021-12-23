from functools import cache
from django.contrib.messages import views
from django.http.response import HttpResponse
from django.shortcuts import render
from django.views.generic import ListView,CreateView,UpdateView,DetailView,View
from front.models import Product, ProductDiscount, ProductSizeWeight, ProductStockManage, ProductSubCategory,ProductCategory, gstPercentage, productGst,productMedia,ProductQuestions,ProductReviews,ProductVarient,ProductAbout,ProductComments,ProductDetails,ProductReviewVoting,ProductTag,ProductTransaction,ProductVariantItems,ProductChildSubCategory
from django.contrib.messages.views import SuccessMessageMixin
from accounts.models import CustomUser, Customers, Merchants, Staffs
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.db.models import Q
from .form import ProductCreateView,ProductChildSubCategoryCreateVIew
from eca.settings import BASE_URL
from django.views.decorators.csrf import csrf_exempt
# Create your views here.


def admin_home(request):
    return render(request,"ecaadmin/home.html")

class ProductCategoryListViews( ):
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

class ProductCategoryTabListViews(ListView):
    model=ProductCategory
    template_name="ecaadmin/category_tab_list.html"
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
        context=super(ProductCategoryTabListViews,self).get_context_data(**kwargs)
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

    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        category =ProductCategory.objects.get(id=self.object.pk)
        context["category"] = category
        return context

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

class ProductSubCategoryTabListViews(ListView):
    model = ProductSubCategory
    template_name = "ecaadmin/subcategory_tab_list.html"
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
        context=super(ProductSubCategoryTabListViews,self).get_context_data(**kwargs)
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

class ProductChildSubCategoryListViews(ListView):
    model = ProductChildSubCategory
    template_name = "ecaadmin/childsubcategory_list.html"
    paginate_by=3

    def get_queryset(self):
        filter_val=self.request.GET.get("filter","")
        order_by=self.request.GET.get("orderby","id")
        if filter_val!="":
            cat=ProductChildSubCategory.objects.filter(Q(title__contains=filter_val) | Q(description__contains=filter_val)).order_by(order_by)
        else:
            cat=ProductChildSubCategory.objects.all().order_by(order_by)

        return cat
   
    def get_context_data(self,**kwargs):
        context=super(ProductChildSubCategoryListViews,self).get_context_data(**kwargs)
        context["filter"]=self.request.GET.get("filter","")
        context["orderby"]=self.request.GET.get("orderby","id")
        context["all_table_fields"]=ProductChildSubCategory._meta.get_fields()
        return context
    
class ProductChildSubCategoryTabListViews(ListView):
    model = ProductChildSubCategory
    template_name = "ecaadmin/childsubcategory_tab_list.html"
    paginate_by=3

    def get_queryset(self):
        filter_val=self.request.GET.get("filter","")
        order_by=self.request.GET.get("orderby","id")
        if filter_val!="":
            cat=ProductChildSubCategory.objects.filter(Q(title__contains=filter_val) | Q(description__contains=filter_val)).order_by(order_by)
        else:
            cat=ProductChildSubCategory.objects.all().order_by(order_by)

        return cat
   
    def get_context_data(self,**kwargs):
        context=super(ProductChildSubCategoryTabListViews,self).get_context_data(**kwargs)
        context["filter"]=self.request.GET.get("filter","")
        context["orderby"]=self.request.GET.get("orderby","id")
        context["all_table_fields"]=ProductChildSubCategory._meta.get_fields()
        return context

class ProductChildSubCategoryUpdate(SuccessMessageMixin,UpdateView):

    def get(self,request,*args,**kwargs):
        product_id=kwargs["pk"]
        pchsbct=ProductChildSubCategory.objects.get(id=product_id)
        categories = ProductCategory.objects.filter(is_active=1)
        categories_list = []
        for category in categories:
            sub_category = ProductSubCategory.objects.filter(is_active=1,category_id=category.id)
            categories_list.append({"category":category,"sub_category":sub_category})
        return render(self.request,"ecaadmin/childsubcategory_update.html",{"pchsbct":pchsbct,"categories":categories_list})

    def post(self,request,*args,**kwargs):
        title=request.POST.get("title")
        description=request.POST.get("description")
        is_active=request.POST.get("is_active")
        thumbnail=request.FILES.get("thumbnail")
        sub_category=request.POST.get("sub_category")

        subcat_obj=ProductSubCategory.objects.get(id=sub_category)
        cat_obj=ProductCategory.objects.get(id=subcat_obj.category.id)
        try:
            pchsbcat_id=kwargs["pk"]
            # pchsbcat=Product.objects.get(id=pchsbcat_id)
            pchsbcat=ProductChildSubCategory.objects.get(id=pchsbcat_id)
            pchsbcat.title=title
            pchsbcat.description=description
            pchsbcat.is_active=is_active
            pchsbcat.subcategory=subcat_obj
            pchsbcat.category=cat_obj
            if thumbnail: 
                fs=FileSystemStorage()
                filename=fs.save(thumbnail.name,thumbnail)
                media_url=fs.url(filename)
                pchsbcat.thumbnail = media_url
                print(media_url)
            pchsbcat.save()
            msg=messages.success(self.request,"Product child subcategory has been Updated Succesfully")
            return HttpResponseRedirect(reverse("childsubcategory_list"))
        except:
            msg=messages.error(request,"Connection Error Try Again")
            return HttpResponseRedirect(reverse("childsubcategory_list"))

class ProductChildSubCategoryCreate(SuccessMessageMixin,CreateView):
    
    def get(self,request,*args,**kwargs):
        form = ProductChildSubCategoryCreateVIew()
        categories = ProductCategory.objects.filter(is_active=1)
        print(categories)
        categories_list = []
        for category in categories:
            sub_category = ProductSubCategory.objects.filter(is_active=1,category_id=category.id)
            categories_list.append({"category":category,"sub_category":sub_category})
        return render(self.request,"ecaadmin/childsubcategory_create.html",{"categories":categories_list,"form":form})

    def post(self,request,*args,**kwargs):
        title=request.POST.get("title")
        description=request.POST.get("description")
        active=request.POST.get("is_active")
        thumbnail=request.FILES.get("thumbnail")
        sub_category=request.POST.get("sub_category")
        product_selling_price=request.POST.get("product_selling_price")
       
 
        subcat_obj=ProductSubCategory.objects.get(id=sub_category)
        cat_obj=ProductCategory.objects.get(id=subcat_obj.category.id)
        is_active= False
        if active == "on":
            is_active = True
        else:
            is_active = False

        try:
            pchsbcat=ProductChildSubCategory(title=title,description=description,is_active=is_active,subcategory=subcat_obj,category=cat_obj)
            pchsbcat.save()
            if thumbnail:
                fs=FileSystemStorage()
                filename=fs.save(thumbnail.name,thumbnail)
                media_url=fs.url(filename)
                pchsbcat.thumbnail = media_url
                pchsbcat.save()
            msg=messages.success(self.request,"Product  child subcategory has been Created Succesfully")
            return HttpResponseRedirect(reverse("childsubcategory_tab_list"))
        except:
            msg=messages.error(request,"Connection Error Try Again")
            return HttpResponseRedirect(reverse("childsubcategory_tab_list"))
 
class MerchantUserCreateView(SuccessMessageMixin,CreateView):
    model = CustomUser
    success_message = "Merchant added !"
    template_name = "ecaadmin/merchant_create.html"
    fields = ['first_name','last_name','email','phone','username','password']

    def form_valid(self, form):
        user = form.save(commit=False)# this will not not WORK WITH auto intense
        # username=self.request.POST.get("username")
        # password=self.request.POST.get("password")
        # email=self.request.POST.get("email")
        # print(username,password,email)
        # user=CustomUser.objects.create_user(username=username,password=password,email=email)
        user.is_active=True
        user.user_type = 4
        user.set_password(form.cleaned_data["password"])
        # user.phone=self.request.POST.get("phone")
        # user.first_name=self.request.POST.get("first_name")
        # user.last_name=self.request.POST.get("last_name")
        user.save()

        profile_pic=self.request.FILES['profile_pic']
        fs=FileSystemStorage()
        filename=fs.save(profile_pic.name,profile_pic)
        profile_pic_url = fs.url(filename)

        # print(profile_pic_url)

        # print(user.merchants)
        # merchants = Merchants.objects.get(admin=user.id)
        # print(merchant)
        user.merchants.profile_pic=profile_pic_url
        user.merchants.company_name=self.request.POST.get("company_name")
        user.merchants.gts_number=self.request.POST.get("gts_number")
        user.merchants.address=self.request.POST.get("address")
        # merchants.user_type=4

        is_added_by_admin = False

        if self.request.POST.get("is_added_by_admin") == "on":
            is_added_by_admin=True
        user.merchants.is_added_by_admin=is_added_by_admin
        user.merchants.save()

        msg=messages.success(self.request,"Merchant Created Succesfully")
        return HttpResponseRedirect(reverse("merchant_tab_list"))
          
class MerchantUserUpdate(SuccessMessageMixin,UpdateView):
    model = CustomUser
    success_message = "Merchant updated !"
    template_name = "ecaadmin/merchant_update.html"
    fields = ['first_name','last_name','email','phone','username','password']

    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        merchant =Merchants.objects.get(admin=self.object.pk)
        context["merchant"] = merchant
        return context

    def form_valid(self, form):
        user = form.save(commit=False) #this will not not WORK WITH auto intense
        user.save()

        merchant  = Merchants.objects.get(admin=user.id)
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

        msg=messages.success(self.request,"Merchant Created Succesfully")
        return HttpResponseRedirect(reverse("merchant_list"))

class MerchantUserListViews(ListView):
    model = Merchants
    template_name = "ecaadmin/merchant_list.html"
    paginate_by=3

class MerchantUserTabListViews(ListView):
    model = Merchants
    template_name = "ecaadmin/merchant_tab_list.html"
    paginate_by=3

    def get_queryset(self):
        filter_val=self.request.GET.get("filter","")
        order_by=self.request.GET.get("orderby","id")
        if filter_val!="":
            cat=Merchants.objects.filter(Q(company_name__contains=filter_val)).order_by(order_by)
        else:
            cat=Merchants.objects.all().order_by(order_by)

        return cat
   
    def get_context_data(self,**kwargs):
        context=super(MerchantUserTabListViews,self).get_context_data(**kwargs)
        context["filter"]=self.request.GET.get("filter","")
        context["orderby"]=self.request.GET.get("orderby","id")
        context["all_table_fields"]=Merchants._meta.get_fields()
        return context

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

class ProductTabListViews(ListView):
    model = Product
    template_name = "ecaadmin/product_tab_list.html"
    paginate_by=3

    def get_queryset(self):
        filter_val=self.request.GET.get("filter","")
        order_by=self.request.GET.get("orderby","id")
        if filter_val!="":
            products=Product.objects.filter(Q(product_name__contains=filter_val) | Q(product_desc__contains=filter_val)).order_by(order_by)
        else:
            products=Product.objects.all().order_by(order_by) 
        print(products)      
        return products
   
    def get_context_data(self,**kwargs):
        context=super(ProductTabListViews,self).get_context_data(**kwargs)
        context["filter"]=self.request.GET.get("filter","")
        context["orderby"]=self.request.GET.get("orderby","id")
        context["all_table_fields"]=Product._meta.get_fields()
        productstocks =ProductStockManage.objects.filter()
        print(productstocks)
        context["productstocks"] = productstocks
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
        childCategory = ProductChildSubCategory.objects.filter(is_active=1)
        print(childCategory)
        return render(request,"ecaadmin/product_update.html",{"categories":categories_list,"product":product,"product_details":product_details,"product_about":product_about,"product_tag":product_tag,"childCategory":childCategory})

    def post(self,request,*args,**kwargs):
        print("i m in product update post")
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

class ProductNewUpdate(View):
    def get(self,request,*args,**kwargs):
        product_id=kwargs["product_id"]
        product=Product.objects.get(id=product_id)
        productmedia = productMedia.objects.filter(product=product_id)
        print(productmedia)
        product_details=ProductDetails.objects.filter(product=product_id)
        product_about=ProductAbout.objects.filter(product=product_id)
        product_tag=ProductTag.objects.filter(product=product_id)
        product_size_weight=ProductSizeWeight.objects.get(product=product_id)
        product_stock=ProductStockManage.objects.get(product=product_id)
        print(product_stock)
        product_gst=productGst.objects.get(product=product_id)
        print(product_gst)
        product_discount=ProductDiscount.objects.filter(product=product_id)

        categories = ProductCategory.objects.filter(is_active=1)
        categories_list = []
        for category in categories:
            sub_category = ProductSubCategory.objects.filter(is_active=1,category_id=category.id)
            categories_list.append({"category":category,"sub_category":sub_category})

        merchants_users=Merchants.objects.filter(admin_id__is_active =True)
        childCategories = ProductChildSubCategory.objects.filter(is_active=1)
        # childsubcategories = ProductChildSubCategory.objects.filter(is_active=1)
        # subcategories_list = []
        # for subcategory in subcategories:
        #     child_sub_category = ProductChildSubCategory.objects.filter(is_active=1,category_id=subcategory.id)
        #     subcategories_list.append({"subcategory":subcategory,"child_sub_category":child_sub_category})
        return render(self.request,"ecaadmin/product_new_update.html",{"product_discount":product_discount,"product_gst":product_gst,"product_stock":product_stock,"product_size_weight":product_size_weight,"product_tag":product_tag,"product_about":product_about,"product_details":product_details,"product":product,"categories":categories_list,'merchants_users':merchants_users,"childCategories":childCategories,"productmedia":productmedia})
        
    def post(self,request,*args,**kwargs):
        product_name=request.POST.get("product_name")
        product_brand=request.POST.get("product_brand")
        product_model_number=request.POST.get("product_model_number")
        product_sku=request.POST.get("product_sku")
        sub_category=request.POST.get("product_subcategory")
        product_childsubcategory=request.POST.get("product_childsubcategory")
        product_mrp=request.POST.get("product_mrp")
        product_selling_price=request.POST.get("product_selling_price")
        product_desc=request.POST.get("product_desc")
        product_weight=request.POST.get("product_weight")
        added_by_merchant=request.POST.get("added_by_merchant")
        in_stock_total=request.POST.get("in_stock_total")
        mini_Quantity=request.POST.get("mini_Quantity")
        media_type_list=request.POST.getlist("media_type[]")
        media_content_list=request.FILES.getlist("media_content[]")
        title_title_list=request.POST.getlist("title_title[]")
        title_details_list=request.POST.getlist("title_details[]")
        about_title_list=request.POST.getlist("about_title[]")
        product_tags=request.POST.get("product_tags")
        product_childsubcategory=request.POST.get("product_childsubcategory")
        product_l_desc=request.POST.get("product_l_desc")
        Out_Of_Stock_Status=request.POST.get("Out_Of_Stock_Status")
        height=request.POST.get("height")
        lenght=request.POST.get("lenght")
        width=request.POST.get("width")
        lenght=request.POST.get("lenght")
        lenght_type=request.POST.get("lenght_type")
        weight_type=request.POST.get("weight_type")
        weight=request.POST.get("weight")
        gst_percentage=request.POST.get("gst_percentage")
        hsn_number=request.POST.get("hsn_number")
        active=request.POST.get("is_active")
        is_active = False
        if active == "on":
            is_active = True
        else:
            is_active= False
        price_list=request.POST.getlist("price[]")
        start_date_list=request.POST.getlist("start_date[]")
        end_date_list=request.POST.getlist("end_date[]")
        quantity_list=request.POST.getlist("quantity[]")
        details_ids=request.POST.getlist("details_id[]")
        about_ids=request.POST.getlist("about_id[]")
        quantity_ids=request.POST.getlist("quantity_id[]")
        
       
        child_subcat_obj=ProductChildSubCategory.objects.get(id=product_childsubcategory)
        subcat_obj=ProductSubCategory.objects.get(id=sub_category)
        cat_obj=ProductCategory.objects.get(id=subcat_obj.category.id)
        print(cat_obj)
        print(subcat_obj)
        print(child_subcat_obj)
        merchant_user_obj=Merchants.objects.get(id=added_by_merchant)
        try:
            product_id=kwargs["product_id"]
            product=Product.objects.get(id=product_id)
            product.product_name=product_name
            product.product_brand=product_brand
            product.product_model_number=product_model_number
            product.product_category=cat_obj
            product.product_subcategory=subcat_obj
            product.product_mrp=product_mrp
            product.product_selling_price=product_selling_price
            product.product_childsubcategory=child_subcat_obj
            product.product_desc=product_desc
            product.added_by_merchant=merchant_user_obj
            product.product_l_desc=product_l_desc
            product.product_sku=product_sku
            product.is_active=is_active    
            product.save()
            print("product saved")

            product_size_weight=ProductSizeWeight.objects.get(product=product)
            product_size_weight.lenght=lenght
            product_size_weight.width=width
            product_size_weight.height=height
            product_size_weight.weight=weight
            product_size_weight.lenght_type=lenght_type
            product_size_weight.weight_type=weight_type
            product_size_weight.product=product
            product_size_weight.save()
            print("Weight saved")

            product_stock=ProductStockManage.objects.get(product=product)
            product_stock.in_stock_total=in_stock_total
            product_stock.mini_Quantity=mini_Quantity
            product_stock.Out_Of_Stock_Status=Out_Of_Stock_Status
            product_stock.product=product
            product_stock.save()
            print("Stock saved")

            
            product_GST =productGst.objects.get(product=product)
            product_GST.product=product
            product_GST.percentage=gst_percentage
            product_GST.hsn_number=hsn_number
            product_GST.save()
            print("GST saved")

            i=0
            if media_content_list:
                for media_content in media_content_list:
                    fs=FileSystemStorage()
                    filename=fs.save(media_content.name,media_content)
                    media_url=fs.url(filename)
                    print("inside images") 
                    # print(media_content[1],"gjkbdgjdfg")
                    pd=Product.objects.get(id=product_id)
                    print(pd.product_image)
                    if pd.product_image:
                        pass
                    else:
                        if media_type_list[0]:
                            pd.product_image=media_url
                            print("inside zero in images")                    
                            pd.save()
                    # if media_type_list[1]:
                    #     product.product_image=media_url
                    #     print("inside one in images")                    
                    #     product.save()
                    product_media = productMedia(product=product,media_type=media_type_list[i],media_content=media_url)
                    product_media.save()
                    print("image saved")
                    i=i+1            

            j=0
            for title_title in title_title_list:
                detail_id=details_ids[j]
                if detail_id == "blank" and title_title != "":
                    print(detail_id,title_title)
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
            print("deatiled saved")


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
            print("about saved")

            l=0
            if quantity_list:
                print(quantity_list)
                for quantity in quantity_list:
                    quantity_id=quantity_ids[l]
                    if quantity_id == "blank" and quantity != "":
                        product_discount=ProductDiscount(quantity=quantity,price=price_list[l],start_date=start_date_list[l],end_date=end_date_list[l],product=product)
                        product_discount.save()
                    else:
                        if quantity != "":
                            product_discount=ProductDiscount.objects.get(id=quantity_id)
                            product_discount.quantity=quantity
                            product_discount.price=price_list[l]            
                            product_discount.start_date=start_date_list[l]            
                            product_discount.end_date=end_date_list[l]            
                            product_discount.save()
                    l=l+1
            print("Discount saved")

            ProductTag.objects.filter(product=product_id).delete()
            product_tags_list=product_tags.split(",")

            for product_tag in product_tags_list:
                product_tag_obj=ProductTag(product_tags=product_tag,product=product)
                product_tag_obj.save()
            print("all data stored")
            msg=messages.success(self.request,"Product Updated Succesfully")
            # return HttpResponse("ok")
            return HttpResponse("Ok")
        except:
            msg=messages.error(request,"Connection Error Try Again")
            # return HttpResponse("error in connection")
            return HttpResponse("Failed")

class ProductView(View):
    def get(self,request,*args,**kwargs):
        form=ProductCreateView()
        categories = ProductCategory.objects.filter(is_active=1)
        categories_list = []
        for category in categories:
            sub_category = ProductSubCategory.objects.filter(is_active=1,category_id=category.id)
            categories_list.append({"category":category,"sub_category":sub_category})
        # for category in categories:
        #     sub_categories = ProductSubCategory.objects.filter(is_active=1,category_id=category.id)
        #     for sub_category in sub_categories:
        #         child_sub_category = ProductChildSubCategory.objects.filter(is_active=1,subcategory_id=sub_category.id)
        #         categories_list.append({"category":category,"sub_categories":sub_categories})
        merchants_users=Merchants.objects.filter(admin_id__is_active =True)
        # allchldct=[]
        # chcattosbcat=ProductChildSubCategory.objects.values('subcategory')
        # subcats={item['subcategory'] for item in chcattosbcat}
        # for subcat in subcats:
        #     chldcat = ProductChildSubCategory.objects.filter(subcategory=subcat,is_active=1)
        #     subcat = ProductSubCategory.objects.filter(id=subcat,is_active=1)
        #     allchldct.append([chldcat,subcat])
        childCategories = ProductChildSubCategory.objects.filter(is_active=1)
        return render(self.request,"ecaadmin/product_create.html",{"categories":categories_list,'merchants_users':merchants_users,'form':form,'childCategories':childCategories})
        
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
        product_childsubcategory=request.POST.get("child_sub_cat")
        long_desc=request.POST.get("long_desc")
 
        child_subcat_obj=ProductChildSubCategory.objects.get(id=product_childsubcategory)
        subcat_obj=ProductSubCategory.objects.get(id=sub_category)
        cat_obj=ProductCategory.objects.get(id=subcat_obj.category.id)
        print(cat_obj)
        print(subcat_obj)
        print(child_subcat_obj)
        merchant_user_obj=Merchants.objects.get(id=added_by_merchant)
        try:
            product=Product(product_name=product_name,product_brand=product_brand,product_model_number=product_model_number,product_category=cat_obj,product_subcategory=subcat_obj,product_mrp=product_mrp,product_selling_price=product_selling_price,product_weight=product_weight,product_childsubcategory=child_subcat_obj,product_desc=product_desc,added_by_merchant=merchant_user_obj,product_l_desc=long_desc,in_stock_total=in_stock_total)
            print("product addded")
            print(product_name,product_brand,product_model_number,cat_obj,subcat_obj,product_mrp,product_selling_price,product_weight,product_desc,merchant_user_obj,long_desc,in_stock_total)
            product.save()
            print("product saved")

            i=0
            for media_content in media_content_list:
                fs=FileSystemStorage()
                filename=fs.save(media_content.name,media_content)
                media_url=fs.url(filename)
                # print(media_content[1],"gjkbdgjdfg")
                if media_type_list[0]:
                    p=Product.objects.get(id=product.id)
                    p.product_image=media_url
                    print("inside zero in images")                    
                    p.save()
                # if media_type_list[1]:
                #     product.product_image=media_url
                #     print("inside one in images")                    
                #     product.save()
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
            print("all data stored")
            msg=messages.success(self.request,"Product Created Succesfully")
            # return HttpResponse("ok")
            return HttpResponseRedirect(reverse("product_list"))
        except:
            msg=messages.error(request,"Connection Error Try Again")
            # return HttpResponse("error in connection")
            return HttpResponseRedirect(reverse("product_list"))

class AddProductView(View):
    def get(self,request,*args,**kwargs):
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
            print(categories_list)
        merchants_users=Merchants.objects.filter(admin_id__is_active =True)
        childCategories = ProductChildSubCategory.objects.filter(is_active=1)
        # childsubcategories = ProductChildSubCategory.objects.filter(is_active=1)
        # subcategories_list = []
        # for subcategory in subcategories:
        #     child_sub_category = ProductChildSubCategory.objects.filter(is_active=1,category_id=subcategory.id)
        #     subcategories_list.append({"subcategory":subcategory,"child_sub_category":child_sub_category})
        print(categories_list)
        return render(self.request,"ecaadmin/add_product.html",{"categories":categories_list,'merchants_users':merchants_users,"childCategories":childCategories})
        
    def post(self,request,*args,**kwargs):
        product_name=request.POST.get("product_name")
        product_brand=request.POST.get("product_brand")
        product_model_number=request.POST.get("product_model_number")
        product_sku=request.POST.get("product_sku")
        sub_category=request.POST.get("product_subcategory")
        product_childsubcategory=request.POST.get("product_childsubcategory")
        product_mrp=request.POST.get("product_mrp")
        product_selling_price=request.POST.get("product_selling_price")
        product_desc=request.POST.get("product_desc")
        product_weight=request.POST.get("product_weight")
        added_by_merchant=request.POST.get("added_by_merchant")
        in_stock_total=request.POST.get("in_stock_total")
        mini_Quantity=request.POST.get("mini_Quantity")
        media_type_list=request.POST.getlist("media_type[]")
        media_content_list=request.FILES.getlist("media_content[]")
        title_title_list=request.POST.getlist("title_title[]")
        title_details_list=request.POST.getlist("title_details[]")
        about_title_list=request.POST.getlist("about_title[]")
        product_tags=request.POST.get("product_tags")
        product_childsubcategory=request.POST.get("product_childsubcategory")
        product_l_desc=request.POST.get("product_l_desc")
        Out_Of_Stock_Status=request.POST.get("Out_Of_Stock_Status")
        height=request.POST.get("height")
        lenght=request.POST.get("lenght")
        width=request.POST.get("width")
        lenght=request.POST.get("lenght")
        lenght_type=request.POST.get("lenght_type")
        weight_type=request.POST.get("weight_type")
        weight=request.POST.get("weight")
        gst_percentage=request.POST.get("gst_percentage")
        hsn_number=request.POST.get("hsn_number")
        active=request.POST.get("is_active")
        is_active = False
        if active == "on":
            is_active = True
        else:
            is_active= False
        quantity_list=request.POST.getlist("quantity[]")
        price_list=request.POST.getlist("price[]")
        start_date_list=request.POST.getlist("start_date[]")
        end_date_list=request.POST.getlist("end_date[]")

        print(product_childsubcategory)
        child_subcat_obj=ProductChildSubCategory.objects.get(id=product_childsubcategory)
        subcat_obj=ProductSubCategory.objects.get(id=sub_category)
        cat_obj=ProductCategory.objects.get(id=subcat_obj.category.id)
        print(cat_obj)
        print(subcat_obj)
        print(child_subcat_obj)
        merchant_user_obj=Merchants.objects.get(id=added_by_merchant)
        try:
            product=Product(product_name=product_name,product_brand=product_brand,product_model_number=product_model_number,product_category=cat_obj,product_subcategory=subcat_obj,product_mrp=product_mrp,product_selling_price=product_selling_price,product_childsubcategory=child_subcat_obj,product_desc=product_desc,added_by_merchant=merchant_user_obj,product_l_desc=product_l_desc,product_sku=product_sku,is_active=is_active)
            print("product addded")
            product.save()
            print("product saved")

            product_size_weight=ProductSizeWeight(lenght=lenght,width=width,height=height,weight=weight,lenght_type=lenght_type,weight_type=weight_type,product=product)
            product_size_weight.save()
            print("product_size_weight saved")
            product_stock=ProductStockManage(in_stock_total=in_stock_total,mini_Quantity=mini_Quantity,Out_Of_Stock_Status=Out_Of_Stock_Status,product=product)
            product_stock.save()
            print("product_stock saved")
            # gst=gstPercentage.objects.get(id=GST_in_percentage)
            # print(gst)
            print(gst_percentage)
            print(hsn_number)
            print(product)
            # product_gstp=productGst(gst_percentage=gst_percentage,hsn_number=hsn_number,product=product)
            gstp=productGst(product=product,percentage=gst_percentage,hsn_number=hsn_number)
            print("product saved")
            gstp.save()
            print("product_GSt saved")

            i=0
            for media_content in media_content_list:
                fs=FileSystemStorage()
                filename=fs.save(media_content.name,media_content)
                media_url=fs.url(filename)
                # print(media_content[1],"gjkbdgjdfg")
                if media_type_list[0]:
                    p=Product.objects.get(id=product.id)
                    p.product_image=media_url
                    print("inside zero in images")                    
                    p.save()
                # if media_type_list[1]:
                #     product.product_image=media_url
                #     print("inside one in images")                    
                #     product.save()
                product_media = productMedia(product=product,media_type=media_type_list[i],media_content=media_url)
                product_media.save()
                i=i+1            

            j=0
            for title_title in title_title_list:
                product_details=ProductDetails(title=title_title,title_details=title_details_list[j],product=product)
                product_details.save()
                j=j+1
            print("product deatils saved")  
            k=0
            for about in about_title_list:
                product_about=ProductAbout(title=about,product=product)
                product_about.save()
                k=k+1
            print("product About saved") 
            l=0
            print(quantity_list)
            for quantity in quantity_list:
                product_discount=ProductDiscount(quantity=quantity,price=price_list[l],start_date=start_date_list[l],end_date=end_date_list[l],product=product)
                print(quantity,price_list[l],start_date_list[l],end_date_list[l])
                product_discount.save()
                l=l+1

            print("product Discount saved") 
            product_tags_list=product_tags.split(",")

            for product_tag in product_tags_list:
                product_tag_obj=ProductTag(product_tags=product_tag,product=product)
                product_tag_obj.save()

            print("product Discount saved")
            product_transaction=ProductTransaction(product=product,transation_type=1,transation_product_count=in_stock_total,transation_desc="initial item added in stock")
            print("product Transaction saved")
            product_transaction.save()
            print("all data stored")
            msg=messages.success(self.request,"Product Created Succesfully")
            # return HttpResponse("ok")
        except:
            msg=messages.error(request,"Connection Error Try Again")

        products = Product.objects.all()
        return render(request,"ecaadmin/product_tab_list.html",{"products":products})
        
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
            if product.product_image == None:
                if media_type_list[0]:
                    product.product_image=media_url
                    print("inside zero in images")                    
                    product.save()
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
        # os.remove(settings.MEDIA_ROOT.replace("","")+str(product_media.media_content).replace("/","\\"))
        
        product_id=product_media.product.id
        product_media.delete()
        return HttpResponseRedirect(reverse("product_edit_media",kwargs={"product_id":product_id}))

class ProductAddStocks(View):
    def get(self,request,*args,**kwargs):
        product_id=kwargs["product_id"]
        product_stock=ProductStockManage.objects.get(product=product_id)
        return render(request,"ecaadmin/product_add_stocks.html",{"product":product_stock})

    def post(self,request,*args,**kwargs):
        product_id=kwargs["product_id"]
        new_instock=request.POST.get("add_stocks")
        product_stock=ProductStockManage.objects.get(product=product_id)
        old_stocks=product_stock.in_stock_total
        new_stocks=int(new_instock)+int(old_stocks)
        product_stock.in_stock_total=new_stocks
        product_stock.save()
 
        product_obj=Product.objects.get(id=product_id)
        product_transaction=ProductTransaction(product=product_obj,transation_product_count=new_instock,transation_desc="New Product Added",transation_type=1)
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

        user.staffs.profile_pic=profile_pic_url
        user.save()
        msg=messages.success(self.request,"Staff User Created")
        return HttpResponseRedirect(reverse("staff_list"))

class StaffUserUpdateView(SuccessMessageMixin,UpdateView):
    template_name="ecaadmin/staff_update.html"
    model=CustomUser
    fields=["first_name","last_name","email","phone","username",]

    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        staffuser=Staffs.objects.get(admin=self.object.pk)
        context["staffuser"]=staffuser
        return context

    def form_valid(self,form):

        #Saving Custom User Object for Merchant User
        user=form.save(commit=False)
        user.save()

        #Saving Merchant user
        staffuser=Staffs.objects.get(admin=user.id)
        if self.request.FILES.get("profile_pic",False):
            profile_pic=self.request.FILES["profile_pic"]
            fs=FileSystemStorage()
            filename=fs.save(profile_pic.name,profile_pic)
            profile_pic_url=fs.url(filename)
            staffuser.profile_pic=profile_pic_url

        staffuser.save()
        msg=messages.success(self.request,"Staff User Updated")
        return HttpResponseRedirect(reverse("staff_list"))

class GstCreateView(View):
    def get(self,request,*args,**kwargs):
        gstdetails=gstPercentage.objects.filter()
        return render(request,"ecaadmin/gst_create.html",{"gstdetails":gstdetails})  

    def post(self,request,*args,**kwargs):
        gst=request.POST.get("add_gst")
        gstdetails=gstPercentage(gst=gst)
        gstdetails.save()

        msg=messages.success(self.request,"GST Created")
        return HttpResponseRedirect(reverse("gst_create"))


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
        msg=messages.success(self.request,"Customer User Created")
        return HttpResponseRedirect(reverse("customer_list"))

class CustomerUserUpdateView(SuccessMessageMixin,UpdateView):
    template_name="ecaadmin/customer_update.html"
    model=CustomUser
    fields=["first_name","last_name","email","phone","username"]

    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        customeruser=Customers.objects.get(admin=self.object.pk)
        context["CustomerUser"]=customeruser
        return context

    def form_valid(self,form):

        #Saving Custom User Object for Merchant User
        user=form.save(commit=False)
        user.save()

        #Saving Merchant user
        customeruser=Customers.objects.get(admin=user.id)
        if self.request.FILES.get("profile_pic",False):
            profile_pic=self.request.FILES["profile_pic"]
            fs=FileSystemStorage()
            filename=fs.save(profile_pic.name,profile_pic)
            profile_pic_url=fs.url(filename)
            customeruser.profile_pic=profile_pic_url

        customeruser.save()
        msg=messages.success(self.request,"Customer User Updated")
        return HttpResponseRedirect(reverse("customer_list"))


def activeCategory(request,pk):
    try:
        cat = ProductCategory.objects.get(id=pk)
        print(cat)
        cat.is_active =True
        cat.save()
        msg=messages.success(request,"Activated Succesfully")
            # return HttpResponse("ok")
        return HttpResponseRedirect(reverse("category_tab_list"))
    except:
            msg=messages.error(request,"Connection Error Try Again")
            # return HttpResponse("error in connection")
            return HttpResponseRedirect(reverse("category_tab_list"))


def deactiveCategory(request,pk):
    try:
        cat = ProductCategory.objects.get(id=pk)
        cat.is_active =False
        cat.save()
        msg=messages.success(request,"Deactivated Succesfully")
            # return HttpResponse("ok")
        return HttpResponseRedirect(reverse("category_tab_list"))
    except:
            msg=messages.error(request,"Connection Error Try Again")
            # return HttpResponse("error in connection")
            return HttpResponseRedirect(reverse("category_tab_list"))

def activeSubCategory(request,pk):
    try:
        cat = ProductSubCategory.objects.get(id=pk)
        print(cat)
        cat.is_active =True
        cat.save()
        msg=messages.success(request,"Activated Succesfully")
            # return HttpResponse("ok")
        return HttpResponseRedirect(reverse("subcategory_tab_list"))
    except:
            msg=messages.error(request,"Connection Error Try Again")
            # return HttpResponse("error in connection")
            return HttpResponseRedirect(reverse("subcategory_tab_list"))


def deactiveSubCategory(request,pk):
    try:
        cat = ProductSubCategory.objects.get(id=pk)
        cat.is_active =False
        cat.save()
        msg=messages.success(request,"Deactivated Succesfully")
            # return HttpResponse("ok")
        return HttpResponseRedirect(reverse("subcategory_tab_list"))
    except:
            msg=messages.error(request,"Connection Error Try Again")
            # return HttpResponse("error in connection")
            return HttpResponseRedirect(reverse("subcategory_tab_list"))


def activeChildSubCategory(request,pk):
    try:
        cat = ProductChildSubCategory.objects.get(id=pk)
        print(cat)
        cat.is_active =True
        cat.save()
        msg=messages.success(request,"Activated Succesfully")
            # return HttpResponse("ok")
        return HttpResponseRedirect(reverse("childsubcategory_tab_list"))
    except:
            msg=messages.error(request,"Connection Error Try Again")
            # return HttpResponse("error in connection")
            return HttpResponseRedirect(reverse("childsubcategory_tab_list"))


def deactiveChildSubCategory(request,pk):
    try:
        cat = ProductChildSubCategory.objects.get(id=pk)
        cat.is_active =False
        cat.save()
        msg=messages.success(request,"Deactivated Succesfully")
            # return HttpResponse("ok")
        return HttpResponseRedirect(reverse("childsubcategory_tab_list"))
    except:
            msg=messages.error(request,"Connection Error Try Again")
            # return HttpResponse("error in connection")
            return HttpResponseRedirect(reverse("childsubcategory_tab_list"))

def activeMerchant(request,pk):
    try:
        cat = Merchants.objects.get(id=pk)
        cat.admin.is_active =True
        cat.admin.save()
        msg=messages.success(request,"Activated Succesfully")
            # return HttpResponse("ok")
        return HttpResponseRedirect(reverse("merchant_tab_list"))
    except:
            msg=messages.error(request,"Connection Error Try Again")
            # return HttpResponse("error in connection")
            return HttpResponseRedirect(reverse("merchant_tab_list"))


def deactiveMerchant(request,pk):
    try:
        cat = Merchants.objects.get(id=pk)
        cat.admin.is_active =False
        cat.admin.save()
        msg=messages.success(request,"Deactivated Succesfully")
            # return HttpResponse("ok")
        return HttpResponseRedirect(reverse("merchant_tab_list"))
    except:
            msg=messages.error(request,"Connection Error Try Again")
            # return HttpResponse("error in connection")
            return HttpResponseRedirect(reverse("merchant_tab_list"))

def gstDelete(request,pk):
    try:
        # gst_details = productGST.objects.get(id=pk)
        # gst_details.delete()
        msg=messages.success(request,"Deleted  Succesfully")
            # return HttpResponse("ok")
        return HttpResponseRedirect(reverse("gst_create"))
    except:
            msg=messages.error(request,"Connection Error Try Again")
            # return HttpResponse("error in connection")
            return HttpResponseRedirect(reverse("gst_create"))

def activeProduct(request,pk):
    try:
        cat = Product.objects.get(id=pk)
        cat.is_active =True
        cat.save()
        msg=messages.success(request,"Activated Succesfully")
            # return HttpResponse("ok")
        return HttpResponseRedirect(reverse("product_tab_list"))
    except:
            msg=messages.error(request,"Connection Error Try Again")
            # return HttpResponse("error in connection")
            return HttpResponseRedirect(reverse("product_tab_list"))


def deactiveProduct(request,pk):
    try:
        cat = Product.objects.get(id=pk)
        cat.is_active =False
        cat.save()
        msg=messages.success(request,"Deactivated Succesfully")
            # return HttpResponse("ok")
        return HttpResponseRedirect(reverse("product_tab_list"))
    except:
        msg=messages.error(request,"Connection Error Try Again")
        # return HttpResponse("error in connection")
        return HttpResponseRedirect(reverse("product_tab_list"))

# def ProductCategoryDelete(request,pks):
#     try:
#         for pk in pks:
#             cat = ProductCategory.objects.get(id=pk)
#             cat.delete()
#             msg=messages.success(request,"Deleted  Succesfully")
#             # return HttpResponse("ok")
#         return HttpResponseRedirect(reverse("category_tab_list"))
#     except:
#         msg=messages.error(request,"Connection Error Try Again")
#         # return HttpResponse("error in connection")
#         return HttpResponseRedirect(reverse("category_tab_list"))
