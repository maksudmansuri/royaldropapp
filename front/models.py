from django.db import models
from django.contrib.auth import user_logged_in
# from ckeditor_uploader.fields import RichTextUploadingField
# from staff_lms.models import Staffs
from accounts.models import Customers as Customers,CustomUser, Merchants,Staffs
from django.urls import reverse
from django.shortcuts import redirect
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from django.utils.text import slugify

# Create your models   .

class ProductCategory(models.Model):
    id                      =           models.AutoField(primary_key=True)
    title                   =           models.CharField(unique=True,max_length=250)
    slug                    =           models.CharField(max_length=255,default="")
    thumbnail               =           models.FileField(null=True,blank=True)
    description             =           models.TextField(default="")
    created_date            =           models.DateTimeField(auto_now_add=True)
    updated_at              =           models.DateTimeField(auto_now_add=True)
    is_active               =           models.IntegerField(default=1)   


    objects = models.Manager()

    def __str__(self):
        return self.title
        
    class Meta:
        ordering = ["-updated_at"]    
    

    # def get_absolute_url(self):
    #     return redirect('instructor_lesson_add', kwargs={'slug': self.product_slug})
    
    def get_absolute_url(self):
        return reverse("category_list")

def pre_save_ProductCategory_post_receiever(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.title)

pre_save.connect(pre_save_ProductCategory_post_receiever, sender=ProductCategory)

class ProductSubCategory(models.Model):
    id                      =           models.AutoField(primary_key=True)
    category                =           models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    title                   =           models.CharField(unique=True,max_length=255)
    thumbnail               =           models.FileField(default = "")
    slug                    =           models.CharField(max_length=255,default="")
    description             =           models.TextField(default="")
    created_date            =           models.DateTimeField(auto_now_add=True)
    updated_at              =           models.DateTimeField(auto_now_add=True)
    is_active               =           models.IntegerField(default=1)   


    objects = models.Manager()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-updated_at"]

    def get_absolute_url(self):
        return reverse("subcategory_list")
   
def pre_save_ProductSubCategory_post_receiever(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.title)

pre_save.connect(pre_save_ProductSubCategory_post_receiever, sender=ProductSubCategory)


class Product(models.Model):
    id                      =           models.AutoField(primary_key=True)
    product_name            =           models.CharField(unique=True,max_length=255,blank=True,null=True,default="")
    product_subcategory     =           models.ForeignKey(ProductSubCategory,on_delete=models.CASCADE)
    product_category        =           models.ForeignKey(ProductCategory,on_delete=models.CASCADE)
    product_mrp             =           models.IntegerField(blank=True,null=True)
    product_selling_price   =           models.IntegerField(blank=True,null=True)
    added_by_merchant       =           models.ForeignKey(Merchants ,on_delete=models.CASCADE,blank=True,null=True)
    product_brand           =           models.CharField(max_length=255,blank=True,null=True,default="")
    product_image           =           models.ImageField(upload_to="product_main/images", height_field=None, width_field=None, max_length=None,blank=True,null=True)
    # product_video         =           models.FileField(upload_to='instructor/module/session',null=True,blank=True,verbose_name="", default="")
    product_model_number    =           models.CharField(max_length=255,blank=True,null=True,default="") 
    product_weight          =           models.CharField(max_length=255,blank=True,null=True,default="")
    product_desc            =           models.TextField()
    product_l_desc          =           models.TextField()
    product_slug            =           models.CharField(max_length=255,blank=True,null=True,unique=True,default="")
    # product_why_take      =           RichTextUploadingField(blank=True,null=True)
    # is_appiled            =           models.BooleanField(blank=True,null=True,default=False)
    is_active               =           models.IntegerField(default=1)   
    in_stock_total          =           models.IntegerField(default=1)
    created_date            =           models.DateTimeField(auto_now_add=True)
    updated_at              =           models.DateTimeField(auto_now_add=True)
    objects                 =           models.Manager()
 

    def __str__(self):
        return self.product_name

    class Meta:
        ordering = ["-updated_at"]
    
    def get_absolute_url(self):
        return reverse('product_view', kwargs={'slug': self.product_slug})


def pre_save_product_post_receiever(sender, instance, *args, **kwargs):
    if not instance.product_slug:
        instance.product_slug = slugify(instance.product_name)

pre_save.connect(pre_save_product_post_receiever, sender=Product)

class productMedia(models.Model):
    id                      =           models.AutoField(primary_key=True)
    product                 =           models.ForeignKey(Product, on_delete=models.CASCADE)
    media_type              =           models.CharField(max_length=255,default="")
    media_type_choice       =           ((1,"Image"),(2,"Video"))
    media_content           =           models.FileField(choices=media_type_choice,default="")
    is_active               =           models.IntegerField(default=1)   
    created_date            =           models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

    def __str__(self):
        return self.product.product_name

class ProductTransaction(models.Model):
    id                      =           models.AutoField(primary_key=True)
    transaction_type_choises=           ((1,"BUY"),(2,"SELL"))
    product                 =           models.ForeignKey(Product, on_delete=models.CASCADE)
    transation_product_count=           models.IntegerField(default=1)
    transation_type         =           models.CharField(choices=transaction_type_choises,max_length=255,default="")
    transation_desc         =           models.CharField(max_length=255,default="")
    created_date            =           models.DateTimeField(auto_now_add=True)
    updated_at              =           models.DateTimeField(auto_now_add=True)
    objects                 =           models.Manager()

    class Meta:
        ordering = ["-updated_at"]

    
class ProductWishlist(models.Model):
    id                      =           models.AutoField(primary_key=True)
    user                    =           models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title                   =           models.CharField(max_length=255)
    product                 =           models.ForeignKey(Product, on_delete=models.CASCADE)
    total_Wishlist          =           models.IntegerField(default=1)   
    created_date            =           models.DateTimeField(auto_now_add=True)
    updated_at              =           models.DateTimeField(auto_now_add=True)
    objects                 =           models.Manager()

 
class ProductDetails(models.Model):
    id                      =           models.AutoField(primary_key=True)
    title_details           =           models.CharField(max_length=255)
    title                   =           models.CharField(max_length=255)
    product                 =           models.ForeignKey(Product, on_delete=models.CASCADE)
    is_active               =           models.IntegerField(default=1)   
    created_date            =           models.DateTimeField(auto_now_add=True)
    updated_at              =           models.DateTimeField(auto_now_add=True)
    objects                 =           models.Manager()

    def __str__(self):
        return self.product.product_name

    class Meta:
        ordering = ["-updated_at"]

class ProductAbout(models.Model):
    id                      =           models.AutoField(primary_key=True)
    title                   =           models.CharField(max_length=255,default="")
    product                 =           models.ForeignKey(Product, on_delete=models.CASCADE)
    is_active               =           models.IntegerField(default=1)   
    created_date            =           models.DateTimeField(auto_now_add=True)
    updated_at              =           models.DateTimeField(auto_now_add=True)
    objects                 =           models.Manager()

    def __str__(self):
        return self.product.product_name

    class Meta:
        ordering = ["-updated_at"]

class ProductTag(models.Model):
    id                      =           models.AutoField(primary_key=True)
    product_tags            =           models.CharField(max_length=255,default="")
    product                 =           models.ForeignKey(Product, on_delete=models.CASCADE)
    is_active               =           models.IntegerField(default=1)   
    created_date            =           models.DateTimeField(auto_now_add=True)
    updated_at              =           models.DateTimeField(auto_now_add=True)
    objects                 =           models.Manager()

    def __str__(self):
        return self.product.product_name

class ProductQuestions(models.Model):
    id                      =           models.AutoField(primary_key=True)
    user                    =           models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product_question        =           models.TextField(default="")
    product_answer          =           models.TextField(default="")
    product                 =           models.ForeignKey(Product, on_delete=models.CASCADE)
    is_active               =           models.IntegerField(default=1)   
    created_date            =           models.DateTimeField(auto_now_add=True)
    updated_at              =           models.DateTimeField(auto_now_add=True)
    objects                 =           models.Manager()

    class Meta:
        ordering = ['-created_date']

class ProductReviews(models.Model):
    id                      =           models.AutoField(primary_key=True)
    user                    =           models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    Product                 =           models.ForeignKey(Product, on_delete=models.CASCADE)
    is_active               =           models.IntegerField(default=1)   
    ratting                 =           models.CharField(default="5",max_length=255)
    reviews                 =           models.TextField(null=True,blank=True,default="")
    parent                  =           models.ForeignKey('self', on_delete=models.CASCADE,null=True)
    created_date            =           models.DateTimeField(auto_now_add=True,blank=True,null=True)
    updated_at              =           models.DateTimeField(auto_now_add=True)
    objects                 =           models.Manager()

    class Meta:
        ordering = ['-created_date']
 
class ProductReviewVoting(models.Model):
    id                      =           models.AutoField(primary_key=True)
    product_review          =           models.ForeignKey(ProductReviews, on_delete=models.CASCADE)
    user                    =           models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    reviws_images           =           models.FileField(default="")
    is_active               =           models.IntegerField(default=1)
    created_date            =           models.DateTimeField(auto_now_add=True,blank=True,null=True)
    updated_at              =           models.DateTimeField(auto_now_add=True)
    objects                 =           models.Manager()

class ProductVarient(models.Model):
    id                      =           models.AutoField(primary_key=True)
    title                   =           models.CharField(max_length=255)
    created_date            =           models.DateTimeField(auto_now_add=True,blank=True,null=True)
    updated_at              =           models.DateTimeField(auto_now_add=True)
    objects                 =           models.Manager()

class ProductVariantItems(models.Model):
    id                      =           models.AutoField(primary_key=True)
    title                   =           models.CharField(max_length=255,default="")
    product_varient         =           models.ForeignKey(ProductVarient, on_delete=models.CASCADE)
    product                 =           models.ForeignKey(Product, on_delete=models.CASCADE)
    created_date            =           models.DateTimeField(auto_now_add=True,blank=True,null=True)
    updated_at              =           models.DateTimeField(auto_now_add=True)
    objects                 =           models.Manager()
    
class CustomersOrders(models.Model):
    id                      =           models.AutoField(primary_key=True)
    product                 =           models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    product_price           =           models.CharField(max_length=255,default="")
    coupon_Code             =           models.CharField(max_length=255,default="")
    discount_amt            =           models.CharField(max_length=255,default="")
    product_status          =           models.CharField(max_length=255,default="")
    created_date            =           models.DateTimeField(auto_now_add=True,blank=True,null=True)
    updated_at              =           models.DateTimeField(auto_now_add=True)
    objects                 =           models.Manager()

    class Meta:
        ordering = ["-updated_at"]

class OderDeliveryStatus(models.Model):
    id                      = models.AutoField(primary_key=True)
    product                 = models.ForeignKey(Product, on_delete=models.CASCADE)
    status                  = models.CharField(max_length=255,default="")
    status_msg              = models.CharField(max_length=255,default="")
    created_date            = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    updated_at              =           models.DateTimeField(auto_now_add=True)
    objects                 = models.Manager()

    class Meta:
        ordering = ["-updated_at"]

@receiver(post_delete, sender=Product)
def submission_delete(sender, instance, **kwargs):
	instance.image.delete(False)


# class Images(models.Model):
#     post = models.ForeignKey(Post, default=None)
#     image = models.ImageField(upload_to=get_image_filename,
#                               verbose_name='Image')


class Product_Modules(models.Model):
    id=models.AutoField(primary_key=True)
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    module=models.CharField(max_length=500,blank=True,null=True)
    module_desc=models.TextField(blank=True,null=True)
    slug=models.SlugField(blank=True,null=True)
    created_date=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    position=models.IntegerField(default=0)
    objects = models.Manager()

    class Meta:
        ordering = ['position']

    def __str__(self):
        return self.module

def pre_save_module_post_receiever(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.Product + "-" + instance.module)

pre_save.connect(pre_save_module_post_receiever, sender=Product_Modules)

class Product_Session(models.Model):
    id=models.AutoField(primary_key=True)
    module=models.ForeignKey(Product_Modules,on_delete=models.CASCADE)
    session_name=models.CharField(max_length=2150,blank=True,null=True,default="")
    session_desc=models.TextField(blank=True,null=True,default="")
    is_appiled=models.BooleanField(blank=True,null=True,default=False)
    is_verified=models.BooleanField(blank=True,null=True,default=False)
    session_duration=models.CharField(max_length=50,blank=True,null=True,default="")
    product_in_pdf=models.FileField(upload_to="Product_Session/Docs", max_length=100,blank=True,null=True,default="")
    created_date=models.DateTimeField(auto_now_add=True,blank=True,null=True)
    updated_at=models.DateTimeField(auto_now_add=True,blank=True,null=True)
    video_link=models.FileField(max_length=2000, upload_to='instructor/module/session',null=True,blank=True,verbose_name="", default="")
    product_slug=models.CharField(max_length=250,default="",blank=True,null=True)
    position=models.IntegerField(default=0)
    objects = models.Manager()

    class Meta:
        ordering = ['position']

    def __str__(self):
        return self.module.module + self.session_name


def pre_save_session_post_receiever(sender, instance, *args, **kwargs):
    if not instance.product_slug:
        instance.product_slug = slugify(instance.module.product + "-" + instance.module + "-" + instance.session_name)

pre_save.connect(pre_save_session_post_receiever, sender=Product_Session)

class ProductComments(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    session = models.ForeignKey(Product_Session, on_delete=models.CASCADE)
    comment = models.TextField(null=True,blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE,null=True)
    created_date = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    objects = models.Manager()

    class Meta:
        ordering = ['-created_date']

class viewed(models.Model):
    id=models.AutoField(primary_key=True)
    customer=models.ForeignKey(Customers,on_delete=models.CASCADE)
    product=models.CharField(max_length=50,blank=True,null=True)
    module_position=models.CharField(max_length=50,blank=True,null=True)
    session_position=models.CharField(max_length=50,blank=True,null=True)
    created_date=models.DateTimeField(auto_now_add=True,blank=True,null=True)
    updated_at=models.DateTimeField(auto_now_add=True,blank=True,null=True)
    objects = models.Manager()

