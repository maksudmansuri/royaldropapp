from django.db import models
from django.contrib.auth import user_logged_in
from ckeditor_uploader.fields import RichTextUploadingField
from accounts.models import Customers as Customers,CustomUser, CustomersAddress, Merchants,Staffs
from django.urls import reverse
from django.shortcuts import redirect
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from django.utils.text import slugify
from front.compression import CompressedImageField, CompressedImageFieldCat

from eca import settings

# Create your models   .
 
class ProductCategory(models.Model):
    id                      =           models.AutoField(primary_key=True)
    # parent_category_id = models.IntegerField(null=True, blank=True)
    title                   =           models.CharField(unique=True,max_length=64)
    slug                    =           models.CharField(max_length=64,default="")
    thumbnail               =           CompressedImageFieldCat(null=True, default=None, quality=90,blank=True)
    description             =           models.TextField(default="",max_length=256)
    created_date            =           models.DateTimeField(auto_now_add=True)
    updated_at              =           models.DateTimeField(auto_now_add=True)
    is_active               =           models.BooleanField(default=False)   
    # CHOICES                 =           [('M','Male'),('F','Female')]
    # Gender=forms.CharField(label='Gender', widget=forms.RadioSelect(choices=CHOICES))
 
    objects = models.Manager()

    def __str__(self):
        return self.title
        
    class Meta:
        ordering = ["-updated_at"]    
    

    # def get_absolute_url(self):
    #     return redirect('instructor_lesson_add', kwargs={'slug': self.product_slug})
    
    def get_absolute_url(self):
        return reverse("category_tab_list")
    
    @property
    def get_thumbnail_url(self):
        if self.thumbnail and hasattr(self.thumbnail, 'url'):
            return self.thumbnail.url
        else:
            return settings.STATIC_ROOT + "eca_admin/img/news/img01.jpg"

def pre_save_ProductCategory_post_receiever(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.title)

pre_save.connect(pre_save_ProductCategory_post_receiever, sender=ProductCategory)

class ProductSubCategory(models.Model):
    id                      =           models.AutoField(primary_key=True)
    category                =           models.ForeignKey(ProductCategory,related_name="subcategory", on_delete=models.CASCADE)
    title                   =           models.CharField(unique=True,max_length=64)
    thumbnail               =           CompressedImageFieldCat(null=True, default=None, quality=90,blank=True)
    slug                    =           models.CharField(max_length=64)
    description             =           models.TextField(max_length=256,default="",null=True)
    created_date            =           models.DateTimeField(auto_now_add=True)
    updated_at              =           models.DateTimeField(auto_now_add=True)
    is_active               =           models.BooleanField(default=False)  


    objects = models.Manager()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["updated_at"]

    def get_absolute_url(self):
        return reverse("subcategory_tab_list")
    
    @property
    def get_thumbnail_url(self):
        if self.thumbnail and hasattr(self.thumbnail, 'url'):
            return self.thumbnail.url
        else:
            return settings.STATIC_ROOT + "eca_admin/img/news/img01.jpg"
   
def pre_save_ProductSubCategory_post_receiever(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.title)

pre_save.connect(pre_save_ProductSubCategory_post_receiever, sender=ProductSubCategory)


class ProductChildSubCategory(models.Model):
    id                      =           models.AutoField(primary_key=True)
    category                =           models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    subcategory             =           models.ForeignKey(ProductSubCategory,related_name="childcategories", on_delete=models.CASCADE)
    title                   =           models.CharField(unique=True,max_length=64)
    thumbnail               =           CompressedImageFieldCat(null=True, default=None, quality=90,blank=True)
    slug                    =           models.CharField(max_length=64,default="",null=True)
    description             =           models.TextField(max_length=256,default="",null=True)
    created_date            =           models.DateTimeField(auto_now_add=True)
    updated_at              =           models.DateTimeField(auto_now_add=True)
    is_active               =           models.BooleanField(default=False)   


    objects = models.Manager()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-updated_at"]

    def get_absolute_url(self):
        return reverse("childsubcategory_tab_list")
    
    @property
    def get_thumbnail_url(self):
        if self.thumbnail and hasattr(self.thumbnail, 'url'):
            return self.thumbnail.url
        else:
            return settings.STATIC_ROOT + "eca_admin/img/news/img01.jpg"

def pre_save_ProductChildSubCategory_post_receiever(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.title)

pre_save.connect(pre_save_ProductChildSubCategory_post_receiever, sender=ProductChildSubCategory)

class Product(models.Model):
    id                      =           models.AutoField(primary_key=True)
    product_name            =           models.CharField(max_length=500)
    product_sku             =           models.CharField(unique=True,max_length=500)
    product_subcategory     =           models.ForeignKey(ProductSubCategory, related_name="productsubcat",on_delete=models.CASCADE,null=True,blank=True)
    product_childsubcategory=           models.ForeignKey(ProductChildSubCategory, related_name="productchildcat", on_delete=models.CASCADE,null=True,blank=True)
    product_category        =           models.ForeignKey(ProductCategory,related_name="productcat",on_delete=models.CASCADE,null=True,blank=True)
    product_mrp             =           models.DecimalField(max_digits=10, decimal_places=2,default=1.0,null=True)
    product_selling_price   =           models.FloatField(default="",null=True)
    added_by_merchant       =           models.ForeignKey(Merchants ,on_delete=models.CASCADE,null=True,blank=True)
    product_brand           =           models.CharField(max_length=64,blank=True,null=True,default="")
    product_image           =           CompressedImageFieldCat(null=True, default=None, quality=90,blank=True)
    # product_video         =           models.ImageField(upload_to='instructor/module/session',null=True,blank=True,verbose_name="", default="")
    product_model_number    =           models.CharField(max_length=64,blank=True,null=True,default="")
    product_desc            =           models.TextField(max_length=1500,blank=True,null=True,default="")
    product_l_desc          =           models.TextField(max_length=5000,blank=True,null=True,default="")
    product_slug            =           models.CharField(max_length=500,blank=True,null=True,unique=True,default="")
    # product_why_take      =           RichTextUploadingField(blank=True,null=True)
    # is_appiled            =           models.BooleanField(blank=True,null=True,default=False)
    is_active               =           models.BooleanField(default=False) 
    is_exclusive            =           models.BooleanField(default=False) 
    gst_percentage          =           models.DecimalField(max_digits=10, decimal_places=2,default=1.0,null=True,blank=True)
    hsn_number              =            models.CharField(max_length=64,blank=True,null=True,default="")
    created_date            =           models.DateTimeField(auto_now_add=True)
    updated_at              =           models.DateTimeField(auto_now_add=True)
    objects                 =           models.Manager()
 

    def __str__(self):
        return self.product_name

    class Meta:
        ordering = ["-updated_at"]
    
    def get_absolute_url(self):
        return reverse('product_view', kwargs={'slug': self.product_slug})
    
    @property
    def get_product_image_url(self):
        if self.product_image and hasattr(self.product_image, 'url'):
            return self.product_image.url
        else:
            return settings.STATIC_ROOT + "eca_admin/img/news/img01.jpg"

def pre_save_product_post_receiever(sender, instance, *args, **kwargs):
    if not instance.product_slug:
        instance.product_slug = slugify(instance.product_name)

pre_save.connect(pre_save_product_post_receiever, sender=Product)

class productMedia(models.Model):
    id                      =           models.AutoField(primary_key=True)
    product                 =           models.ForeignKey(Product,related_name="productmedia", on_delete=models.CASCADE)
    media_type              =           models.CharField(max_length=255,blank=True,null=True,default="")
    media_type_choice       =           ((1,"Image"),(2,"Video"))
    media_content           =           CompressedImageField(null=True, default=None, quality=60,blank=True)
    is_active               =           models.BooleanField(default=False)     
    created_date            =           models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

    # def __str__(self):
    #     return self.product.product_name
    @property
    def get_media_content_url(self):
        if self.media_content and hasattr(self.media_content, 'url'):
            return self.media_content.url
        else:
            return settings.STATIC_ROOT + "eca_admin/img/news/img01.jpg"

class gstPercentage(models.Model):
    id                      =           models.AutoField(primary_key=True)
    gst                     =           models.CharField(max_length=16,null=True)    
    created_date            =           models.DateTimeField(auto_now_add=True)
    updated_at              =           models.DateTimeField(auto_now_add=True)
    objects                 =           models.Manager()
    
    def __str__(self):
        return self.gst
    
    class Meta:
        ordering = ["updated_at"]

class productGst(models.Model):
    id                      =           models.AutoField(primary_key=True)
    product                 =           models.ForeignKey(Product,related_name="productgst",  on_delete=models.CASCADE)
    GST_CHOISES             =           ((1,'0%'),(2,'3%'),(3,'5%'),(4,'12%'),(5,'18%'),(6,'28%'))
    percentage              =           models.CharField(max_length=255,blank=True,null=True,default="")
    gst_percentage          =           models.CharField(max_length=256,default="",null=True)
    hsn_number              =           models.CharField(max_length=256,default="",null=True)  
    created_date            =           models.DateTimeField(auto_now_add=True)
    updated_at              =           models.DateTimeField(auto_now_add=True)
    objects                 =           models.Manager()

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
    title                   =           models.CharField(max_length=64)
    product                 =           models.ForeignKey(Product, on_delete=models.CASCADE)
    total_Wishlist          =           models.IntegerField(default=1)   
    created_date            =           models.DateTimeField(auto_now_add=True)
    updated_at              =           models.DateTimeField(auto_now_add=True)
    objects                 =           models.Manager()

class ProductMetaTag(models.Model):
    id                      =           models.AutoField(primary_key=True)
    title_details           =           models.CharField(max_length=255,blank=True,null=True,default="")
    title                   =           models.CharField(max_length=64,blank=True,null=True,default="")
    product                 =           models.ForeignKey(Product, on_delete=models.CASCADE)
    is_active               =           models.BooleanField(default=False)     
    created_date            =           models.DateTimeField(auto_now_add=True)
    updated_at              =           models.DateTimeField(auto_now_add=True)
    objects                 =           models.Manager()

    def __str__(self):
        return self.product.product_name

    class Meta:
        ordering = ["-updated_at"]

class ProductSizeWeight(models.Model):
    id                      =           models.AutoField(primary_key=True)
    lenght                  =           models.IntegerField(blank=True,null=True,default="")
    width                   =           models.IntegerField(blank=True,null=True,default="")
    height                  =           models.IntegerField(blank=True,null=True,default="")
    weight                  =           models.FloatField(blank=True,null=True,default="")
    lenght_type_choice      =           ((1,"Inch"),(2,"Centimeter"))
    lenght_type             =           models.CharField(max_length=16,choices=lenght_type_choice,default="")
    weight_type_choice      =           ((1,"Gram"),(2,"Kilogram"))
    weight_type             =           models.CharField(max_length=16,choices=lenght_type_choice,default="")
    product                 =           models.ForeignKey(Product,related_name="productsizeweight", on_delete=models.CASCADE)
    is_active               =           models.BooleanField(default=False)     
    created_date            =           models.DateTimeField(auto_now_add=True)
    updated_at              =           models.DateTimeField(auto_now_add=True)
    objects                 =           models.Manager()

    def __str__(self):
        return self.product.product_name

    class Meta:
        ordering = ["-updated_at"]

class ProductStockManage(models.Model):
    id                      =           models.AutoField(primary_key=True)
    in_stock_total          =           models.IntegerField(default=1)
    mini_Quantity           =           models.IntegerField(blank=True,null=True,default=1)
    stock_type_choice       =           ((1,"available"),(2,"Out Of Stock"),(3,"Product Discontinued"))
    Out_Of_Stock_Status     =           models.CharField(max_length=64,choices=stock_type_choice,default="")
    product                 =           models.ForeignKey(Product,related_name="productstockmanage", on_delete=models.CASCADE)
    is_active               =           models.BooleanField(default=False)     
    created_date            =           models.DateTimeField(auto_now_add=True)
    updated_at              =           models.DateTimeField(auto_now_add=True)
    objects                 =           models.Manager()

    def __str__(self):
        return self.product.product_name

    class Meta:
        ordering = ["-updated_at"]

class ProductDetails(models.Model):
    id                      =           models.AutoField(primary_key=True)
    title_details           =           models.CharField(max_length=256,default="")
    title                   =           models.CharField(max_length=64,default="")
    product                 =           models.ForeignKey(Product, related_name="productdetails", on_delete=models.CASCADE)
    is_active               =           models.BooleanField(default=False)     
    created_date            =           models.DateTimeField(auto_now_add=True)
    updated_at              =           models.DateTimeField(auto_now_add=True)
    objects                 =           models.Manager()

    def __str__(self):
        return self.product.product_name

    class Meta:
        ordering = ["-updated_at"]

class ProductAbout(models.Model):
    id                      =           models.AutoField(primary_key=True)
    title                   =           models.CharField(max_length=256,default="")
    product                 =           models.ForeignKey(Product,related_name="productabout", on_delete=models.CASCADE)
    is_active               =           models.BooleanField(default=False)     
    created_date            =           models.DateTimeField(auto_now_add=True)
    updated_at              =           models.DateTimeField(auto_now_add=True)
    objects                 =           models.Manager()

    def __str__(self):
        return self.product.product_name

    class Meta:
        ordering = ["-updated_at"]

class ProductTag(models.Model):
    id                      =           models.AutoField(primary_key=True)
    product_tags            =           models.CharField(max_length=256,default="")
    product                 =           models.ForeignKey(Product,related_name="producttag", on_delete=models.CASCADE)
    is_active               =           models.BooleanField(default=False)     
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
    is_active               =           models.BooleanField(default=False)     
    created_date            =           models.DateTimeField(auto_now_add=True)
    updated_at              =           models.DateTimeField(auto_now_add=True)
    objects                 =           models.Manager()

    class Meta:
        ordering = ['-created_date']

class ProductReviews(models.Model):
    id                      =           models.AutoField(primary_key=True)
    user                    =           models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product                 =           models.ForeignKey(Product,related_name="productreviews", on_delete=models.CASCADE)
    is_active               =           models.BooleanField(default=False)    
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
    reviws_images           =           CompressedImageField(null=True, default=None, quality=60,blank=True)
    is_active               =           models.BooleanField(default=False)  
    created_date            =           models.DateTimeField(auto_now_add=True,blank=True,null=True)
    updated_at              =           models.DateTimeField(auto_now_add=True)
    objects                 =           models.Manager()

    @property
    def get_photo_url(self):
        if self.reviws_images and hasattr(self.reviws_images, 'url'):
            return self.reviws_images.url
        else:
            return settings.STATIC_ROOT + "eca_admin/img/news/img01.jpg"

class ProductVarient(models.Model):
    id                      =           models.AutoField(primary_key=True)
    title                   =           models.CharField(max_length=255,default="")
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

class TempOrder(models.Model):
    id                      =           models.AutoField(primary_key=True)
    amount                  =           models.DecimalField(max_digits=10, decimal_places=2,default=1.0,null=True,blank=True)
    product                 =           models.CharField(default="",max_length=5000)
    quantity                =           models.IntegerField()
    address                 =           models.ForeignKey(CustomersAddress, on_delete=models.CASCADE,default="")
    customer                =           models.ForeignKey(Customers,on_delete=models.CASCADE,default="")
    created_date            =           models.DateTimeField(auto_now_add=True,blank=True,null=True)
    updated_at              =           models.DateTimeField(auto_now_add=True)
    objects                 =           models.Manager()

    class Meta:
        ordering = ["-updated_at"]

class Orders(models.Model):
    id                      =           models.AutoField(primary_key=True)
    product_Json            =           models.CharField(max_length=5000,default="")
    amount                  =           models.DecimalField(max_digits=10, decimal_places=2,default=1.0)
    payment_method          =           models.CharField(max_length=256,default="")
    address                 =           models.ForeignKey(CustomersAddress, on_delete=models.CASCADE,default="")
    status                  =           models.CharField(max_length=256,default="",blank=True,null=True)
    transaction_id          =           models.CharField(max_length=256,default="",blank=True,null=True)
    customer                =           models.ForeignKey(Customers,on_delete=models.CASCADE,default="",)
    created_date            =           models.DateTimeField(auto_now_add=True,blank=True,null=True)
    updated_at              =           models.DateTimeField(auto_now_add=True)
    objects                 =           models.Manager()

    class Meta:
        ordering = ["-updated_at"]

class CustomersOrders(models.Model):
    id                      =           models.AutoField(primary_key=True)
    product                 =           models.ForeignKey(Product, on_delete=models.CASCADE)
    customersaddress        =           models.ForeignKey(CustomersAddress,on_delete=models.CASCADE)
    customer                =           models.ForeignKey(Customers,on_delete=models.CASCADE)
    product_price           =           models.CharField(max_length=255,default="")
    product_quantity        =           models.CharField(max_length=255,default="")
    coupon_Code             =           models.CharField(max_length=255,default="")
    discount_amt            =           models.CharField(max_length=255,default="")
    status_type_choice      =           (("O","Ordered"),("C","Cancelled "),("P","Pending"))
    order_status            =           models.CharField(max_length=255,default="",choices=status_type_choice)
    created_date            =           models.DateTimeField(auto_now_add=True,blank=True,null=True)
    updated_at              =           models.DateTimeField(auto_now_add=True)
    objects                 =           models.Manager()

    class Meta: 
        ordering = ["-updated_at"]

class OrderTacker(models.Model):
    id                      =           models.AutoField(primary_key=True)
    ordes_id                =           models.IntegerField()
    desc                    =           models.CharField(max_length=5000)
    created_date            =           models.DateTimeField(auto_now_add=True,blank=True,null=True)
    updated_at              =           models.DateTimeField(auto_now_add=True)
    objects                 =           models.Manager()

class OderDeliveryStatus(models.Model):
    id                      =           models.AutoField(primary_key=True)
    Ordes_id                =           models.ForeignKey(CustomersOrders, on_delete=models.CASCADE,default="")
    product                 =           models.ForeignKey(Product, on_delete=models.CASCADE,default="")
    status                  =           models.CharField(max_length=255,default="")
    status_type_choice      =           (("Pr","Prosesing"),("On","On the Way "),("D","Delivered"))
    status_msg              =           models.CharField(max_length=255,default="",choices=status_type_choice)
    created_date            =           models.DateTimeField(auto_now_add=True,blank=True,null=True)
    updated_at              =           models.DateTimeField(auto_now_add=True)
    objects                 =           models.Manager()

    class Meta:
        ordering = ["-updated_at"]

class ProductCouponCode(models.Model):
    id                      =           models.AutoField(primary_key=True)
    product                 =           models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity                =           models.IntegerField(default="",null=True)
    price                   =           models.IntegerField(null=True)
    start_date              =           models.DateField(default="",null=True)
    end_date                =           models.DateField(default="",null=True)
    is_active               =           models.BooleanField(default=False)  
    created_date            =           models.DateTimeField(auto_now_add=True,blank=True,null=True)
    updated_at              =           models.DateTimeField(auto_now_add=True)
    objects                 =           models.Manager()

class ProductDiscount(models.Model):
    id                      =           models.AutoField(primary_key=True)
    product                 =           models.ForeignKey(Product, related_name="productdiscount", on_delete=models.CASCADE)
    quantity                =           models.IntegerField(default="",null=True)
    price                   =           models.IntegerField(null=True)
    start_date              =           models.DateField(default="",null=True)
    end_date                =           models.DateField(default="",null=True)
    is_active               =           models.BooleanField(default=False)  
    created_date            =           models.DateTimeField(auto_now_add=True,blank=True,null=True)
    updated_at              =           models.DateTimeField(auto_now_add=True)
    objects                 =           models.Manager()

    class Meta:
        ordering = ["-updated_at"]

# @receiver(post_delete, sender=Product)
# def submission_delete(sender, instance, **kwargs):
# 	instance.image.delete(False)


# class Images(models.Model):
#     post = models.ForeignKey(Post, default=None)
#     image = models.ImageField(upload_to=get_image_filename,
#                               verbose_name='Image')
