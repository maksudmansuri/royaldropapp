from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
from django.db import models
from django.db.models.fields import AutoField
from django.db.models.signals import post_save
from django.dispatch import receiver
# from ckeditor_uploader.fields import RichTextUploadingField
from rest_framework.authtoken.models import Token
from django.conf import settings
from django.core.validators import RegexValidator
from django.db.models import Q
# Create your models here.

# class CustomUser(AbstractUser): 
#     user_type_data=((1,"HOD"),(2,"Staff"),(3,"Customer"))
#     user_type=models.CharField(choices=user_type_data,max_length=10)

class MyAccountManager(BaseUserManager):
    # create _create_user for mobiel number for facebbook and for google and for userid password so it can be solve your all problem regarding social login/auth
    use_in_migrations = True
    def create_user(self, email, username,password=None):
        if not email:
            pass
            raise ValueError("User must have an Email Address")
        if not username:
            raise ValueError("User must have an username ")

        user = self.model(
                email=self.normalize_email(email),
                username=username,                
               
            )
        user.is_active= True
        user.set_password(password)
        print(user.username)
        user.save(using=self._db)
        print(user.email)
        return user

    def create_superuser(self, email, username, password,**extra_fields):
        user = self.create_user(
                email=self.normalize_email(email),
                password=password,
                username=username,
                            
                
            )
        
        # phone = "7801925101"
        user.is_active = True
        # user.is_admin = True
        # user_type="0"
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class CustomUser(AbstractBaseUser): 
    email = models.EmailField(verbose_name="email", max_length=254, unique=True)
    username = models.CharField(max_length=254,unique=True)
    date_joined = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="date joined" ,auto_now=True)
    # is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    first_name = models.CharField(max_length=254)
    last_name = models.CharField(max_length=254)
    user_type_data=((1,"Admin"),(2,"Staff"),(3,"Customer"),(4 ,"Merchant"))
    user_type=models.CharField(choices=user_type_data,max_length=10)
    phone_regex     = RegexValidator( regex = r'^\+?1?\d{9,10}$', message ="Phone number must be entered in the format +919999999999. Up to 10 digits allowed.")
    phone           = models.CharField('Phone',validators =[phone_regex], max_length=10, unique = True,null=True)
    
    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['username',]

    objects = MyAccountManager()

    def __str__(self):
        return self.email
    
    def has_perm(self,perm,obj=None):
        return self.is_superuser

    def has_module_perms(self,app_label):
        return True    

class PhoneOTP(models.Model):
    
    # id=models.AutoField(primary_key=True)
    # admin=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    phone_regex     = RegexValidator( regex = r'^\+?1?\d{9,10}$', message ="Phone number must be entered in the format +919999999999. Up to 14 digits allowed.")
    phone           = models.CharField(validators =[phone_regex], max_length=17, unique = True)
    otp             = models.CharField(max_length=9, blank = True, null=True)
    count           = models.IntegerField(default=0, help_text = 'Number of otp_sent')
    validated       = models.BooleanField(default = False, help_text = 'If it is true, that means user have validate otp correctly in second API')
    otp_session_id  = models.CharField(max_length=120, null=True, default = "")
    username        = models.CharField(max_length=20, blank = True, null = True, default = None )
    email           = models.CharField(max_length=50, null = True, blank = True, default = None) 
    password        = models.CharField(max_length=100, null = True, blank = True, default = None) 

    

    def __str__(self):
        return str(self.phone) + ' is sent ' + str(self.otp)   

class AdminHOD(models.Model):
    id=models.AutoField(primary_key=True)
    admin=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    profile_pic = models.FileField(default = "")
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()

class Staffs(models.Model):
    id=models.AutoField(primary_key=True)
    admin=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    first_name=models.CharField(max_length=250,default="",null=True)
    last_name=models.CharField(max_length=250,default="",null=True)
    dob=models.DateField(blank=True,null=True)
    address=models.CharField(max_length=50,blank=True,null=True)
    city=models.CharField(max_length=50,blank=True,null=True)
    state=models.CharField(max_length=50,blank=True,null=True)
    country=models.CharField(max_length=50,blank=True,null=True)
    # mobile=models.CharField(max_length=50,blank=True,null=True)
    # qualification=models.CharField(max_length=50,blank=True,null=True)
    # specialist=models.CharField(max_length=50,blank=True,null=True)
    profile_pic=models.FileField(upload_to="instructor/profile",null=True,default="")
    # about=RichTextUploadingField(blank=True,null=True)
    # is_appiled=models.BooleanField(blank=True,null=True,default=False)
    is_verified=models.BooleanField(blank=True,null=True,default=False)
    # resume=models.FileField(upload_to="instructor/resume", max_length=250,blank=True,null=True)
    # experience=models.CharField(max_length=50,blank=True,null=True)
    # working_with=models.CharField(max_length=50,blank=True,null=True)
    # website=models.URLField(max_length=200,blank=True,null=True)
    # linkdin=models.URLField(max_length=200,blank=True,null=True)
    gender=models.CharField(max_length=200,blank=True,null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)

    objects=models.Manager()
    
    def __str__(self):
        return self.first_name  
 
class Customers(models.Model):
    id=models.AutoField(primary_key=True)
    admin=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    fisrt_name=models.CharField(max_length=250,blank=True,null=True)
    last_name=models.CharField(max_length=250,blank=True,null=True)
    address=models.CharField(max_length=500,blank=True,null=True)
    city=models.CharField(max_length=250,blank=True,null=True)
    state=models.CharField(max_length=250,blank=True,null=True)
    country=models.CharField(max_length=250,blank=True,null=True)
    zip_Code =models.CharField(max_length=250,blank=True,null=True)
    # qualification =models.CharField(max_length=250,blank=True,null=True)
    dob=models.DateField(blank=True,null=True)
    phone=models.CharField(max_length=250,blank=True,null=True)
    profile_pic=models.FileField(upload_to="customer_lms/profile/images",blank=True,null=True)
    gender=models.CharField(max_length=255,null=True)
    # is_appiled=models.BooleanField(blank=True,null=True,default=False)
    # is_verified=models.BooleanField(blank=True,null=True,default=False)
    # session_start=models.DateField(null=True)
    # session_end=models.DateField(null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects = models.Manager()
 
class CustomersAddress(models.Model):  
    id=models.AutoField(primary_key=True)
    customer=models.ForeignKey(Customers,on_delete=models.CASCADE)
    fisrt_name=models.CharField(max_length=250,blank=True,null=True,default="")
    last_name=models.CharField(max_length=250,blank=True,null=True,default="")
    address=models.CharField(max_length=500,blank=True,null=True,default="")
    city=models.CharField(max_length=250,blank=True,null=True,default="")
    state=models.CharField(max_length=250,blank=True,null=True,default="")
    country=models.CharField(max_length=250,blank=True,null=True,default="")
    zip_Code =models.CharField(max_length=250,blank=True,null=True)       
    phone=models.CharField(max_length=250,blank=True,null=True,default="")
    is_active = models.BooleanField(blank=True,null=True,default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects = models.Manager()
 
class Merchants(models.Model):
    id=models.AutoField(primary_key=True)
    admin=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    company_register_year = models.DateField(blank=True,null=True)
    company_name = models.CharField(max_length=255)
    gts_number =  models.CharField(max_length=255)
    address=models.TextField(max_length=500,blank=True,null=True)
    city=models.CharField(max_length=250,blank=True,null=True)
    state=models.CharField(max_length=250,blank=True,null=True,default="Gujarat")
    country=models.CharField(max_length=250,blank=True,null=True,default="India")
    profile_pic=models.FileField(upload_to="Merchant/images",blank=True,null=True)
    zip_code=models.CharField(max_length=250,blank=True,null=True,default="")
    is_added_by_admin=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    is_verified=models.BooleanField(blank=True,null=True,default=False)
    website=models.URLField(max_length=200,blank=True,null=True,default="www.google.com")

    objects = models.Manager()

class userPayment(models.Model):
    id=models.AutoField(primary_key=True)
    customers=models.ForeignKey(Customers, on_delete=models.CASCADE)
    payment_type=models.CharField(max_length=50)
    payment_provider = models.CharField(max_length=50)
    account_info =models.IntegerField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)




@receiver(post_save,sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender,instance=None,created=False,**kwargs):
    if created:
        Token.objects.create(user=instance)

# @receiver(post_save,sender=Customers)
# def create_user_profile(sender,instance,created,**kwargs):
#     if created:
#         CustomersAddress.objects.create(customer=instance)
#             # Customers.objects.create(admin=instance,product_id=Products.objects.get(id=1),session_start_year="2020-01-01",session_end_year="2021-01-01",address="",profile_pic="",gender="")

# @receiver(post_save,sender=Customers)
# def save_user_profile(sender,instance,**kwargs):
#     instance.customersaddress.save()

@receiver(post_save,sender=CustomUser)
def create_user_profile(sender,instance,created,**kwargs):
    if created:
        if instance.user_type==1:
            AdminHOD.objects.create(admin=instance)
        if instance.user_type==2:
            Staffs.objects.create(admin=instance)
        if instance.user_type==3:
            Customers.objects.create(admin=instance)
        if instance.user_type==4:
            Merchants.objects.create(admin=instance)
            # Customers.objects.create(admin=instance,product_id=Products.objects.get(id=1),session_start_year="2020-01-01",session_end_year="2021-01-01",address="",profile_pic="",gender="")

@receiver(post_save,sender=CustomUser)
def save_user_profile(sender,instance,**kwargs):
    if instance.user_type==1:
        instance.adminhod.save()
    if instance.user_type==2:
        instance.staffs.save()
    if instance.user_type==3:
        instance.customers.save()
    if instance.user_type==4:
        instance.merchants.save()