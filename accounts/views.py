import datetime
import random 
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404, render,redirect,HttpResponseRedirect
from django.views.generic.edit import CreateView
from .models import CustomUser
from accounts.EmailBackEnd import EmailBackEnd
from django.contrib.auth import login,logout,authenticate
from django.contrib.sessions.models import Session
from django.contrib.auth.decorators import login_required 
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes,force_str,DjangoUnicodeDecodeError
from .utils import generate_token
from django.core.mail import EmailMessage
from django.conf import settings
from rest_framework import viewsets
from django.core.files.storage import FileSystemStorage
from django.core.exceptions import ObjectDoesNotExist
#API for Apps
# class CustomUserViewSet(viewsets.ModelViewSet):
#     queryset = CustomUser.objects.all().order_by('username')
#     serializer_class = CustomUserSerializer
  

# Create your views here .gg

# def soc_login(request):
#     return render(request,'dologin')

def send_otp(phone):
    if phone:
        key = random.randint(999,9999)
        return key
    else:
        return False
    
# This class returns the string needed to generate the key
class generateKey:
    @staticmethod
    def returnValue(phone):
        return str(phone) + str(datetime.date(datetime.now())) + "Some Random Secret Key"

def verifyPhone(request,phone):
    try:
        user = CustomUser.objects.get(phone=phone)
        print("inside virify phone")
    except ObjectDoesNotExist:
        messages.add_message(request,messages.ERROR,"Mobile number does not Exits")
        return render(request,"accounts/OTPVerification.html")  # False Call
    return render(request,"accounts/otp-verify.html",{'user':user})  #  Call

def resendOTP(request,phone):
    user = get_object_or_404(CustomUser,phone=phone)
    key = send_otp(phone)
    # OTP = pyotp.HOTP(key)  # HOTP Model for OTP is created
    # print(OTP.at(user.counter))
    # otp=OTP.at(user.counter)
    # conn.request("GET", "https://2factor.in/API/R1/?module=SMS_OTP&apikey=f08f2dc9-aa1a-11eb-80ea-0200cd936042&to="+str(mobile)+"&otpvalue="+str(otp)+"&templatename=WomenMark1")
    # res = conn.getresponse()
    # data = res.read()
    # data=data.decode("utf-8")
    # data=ast.literal_eval(data)
    # print(data)
    # if data["Status"] == 'Success':
    #     user.otp_session_id = data["Details"]
    user.otp = str(key)
    user.save()
        # print('In validate phone :'+user.otp_session_id)
    messages.add_message(request,messages.SUCCESS,"OTP sent successfully") 
    return HttpResponseRedirect(reverse("verifyPhone",kwargs={'phone':user.phone}))

def verifyOTP(request,phone):
    try:
        user = CustomUser.objects.get(phone=phone) #mobile is a user
    except ObjectDoesNotExist:
        messages.add_message(request,messages.ERROR,"Mobile number does not Exits")
        return HttpResponseRedirect(reverse("hospitalsingup"))  # False Call
    if request.POST:
        first=request.POST.get("first")
        second=request.POST.get("second")
        third=request.POST.get("third")
        forth=request.POST.get("forth")
        # fifth=request.POST.get("fifth")
        # sixth=request.POST.get("sixth")

        postotp = first+second+third+forth  #added in one string

        # keygen = generateKey()
        # key = base64.b32encode(keygen.returnValue(phone).encode())  # Generating Key
        key =user.otp  # Generating Key
        # OTP = pyotp.HOTP(user.otp)  # HOTP Model
        #key = CustomUser.objects.get()
        # if OTP.verify(postotp, user.counter):  # Verifying the OTP
        if key == postotp:  # Verifying the OTP
            user.is_Mobile_Verified = True
            user.is_active=True
            user.save()
            messages.add_message(request,messages.SUCCESS,"Mobile Number is VArified Successfully")
        else:
            messages.add_message(request,messages.ERROR,"Incorrect OTP !")
            return HttpResponseRedirect(reverse("verifyPhone",kwargs={'phone':user.phone}))
        #emila message for email verification
        current_site=get_current_site(request) #fetch domain
        print(current_site)   
        email_subject='Active your Account',
        message=render_to_string('accounts/activate.html',
        { 
            'user':user,
            'domain':current_site.domain,
            'uid':urlsafe_base64_encode(force_bytes(user.pk)),
            'token':generate_token.make_token(user)
        } #convert Link into string/message
        )
        print(message)
        email_message=EmailMessage(
            email_subject, 
            message,
            settings.EMAIL_HOST_USER,
            [user.email]
        )#compose email
        print(email_message)
        # email_message.send() #send Email
        messages.add_message(request,messages.SUCCESS,"Sucessfully Singup Please Verify Your Account Email")
        if user is not None:
            if user.is_active == True:
                login(request,user)
                # request.session['logged in']=True
                if user.user_type=="1":
                    if 'next' in request.POST:
                        return redirect(request.POST.get('next'))
                    # elif user.profile_pic:
                    #     return HttpResponseRedirect(reverse('profile_picUpload'))
                    else:
                        return HttpResponseRedirect(reverse('radmin_home'))
                        # return HttpResponseRedirect(reverse('admin:index'))
                if user.user_type=="2":
                    if 'next' in request.POST:
                        return redirect(request.POST.get('next'))
                    # elif user.profile_pic:
                    #     return HttpResponseRedirect(reverse('profile_picUpload'))
                    else: 
                        return HttpResponseRedirect(reverse('hospital_dashboard'))
                elif user.user_type=="3":
                    if 'next' in request.POST:
                        return redirect(request.POST.get('next'))
                    # elif user.profile_pic:
                    #     return HttpResponseRedirect(reverse('profile_picUpload'))
                    else:
                        return HttpResponseRedirect(reverse('admin_home'))
                elif user.user_type=="4":
                    if 'next' in request.POST:
                        return redirect(request.POST.get('next'))
                    # elif user.profile_pic:
                    #     return HttpResponseRedirect(reverse('profile_picUpload'))
                    # print(" i am here but not goinf inside1")
                    # if user.profile_pic == None:
                    #     print(" i am here but not goinf inside2")
                    #     return HttpResponseRedirect(reverse('patientregisterstep1',kwargs={'user_id':user.id}))
                    # elif user.first_name == None:
                    #     print(" i am here but not goinf inside3")
                    #     return HttpResponseRedirect(reverse('patientregisterstep2',kwargs={'user_id':user.id}))
                    # elif user.patients.address == None:
                    #     print(" i am here but not goinf inside4")
                    #     return HttpResponseRedirect(reverse('patientregisterstep3',kwargs={'user_id':user.id}))
                    else:
                        return HttpResponseRedirect(reverse('patient_home'))
                elif user.user_type=="5":
                    if 'next' in request.POST:
                        return redirect(request.POST.get('next'))
                    # elif user.profile_pic:
                    #     return HttpResponseRedirect(reverse('profile_picUpload'))
                    else:
                        return HttpResponseRedirect(reverse('lab_home'))
                elif user.user_type=="6":
                    if 'next' in request.POST:
                        return redirect(request.POST.get('next'))
                    # elif user.profile_pic:
                    #     return HttpResponseRedirect(reverse('profile_picUpload'))
                    else:
                        return HttpResponseRedirect(reverse('pharmacy_home'))
                else:
                # For Djnago default Admin Login 
                    return HttpResponseRedirect(reverse('admin:index'))
                    
                    # return RedirectView.as_view(url=reverse_lazy('admin:index'))
                    # return HttpResponseRedirect(reverse('admin_home'))
            else:
                # message.add_message(request,messages.ERROR,"Please Verify Your Account First")
                return redirect('/accounts/dologin')
        else: 
            # print(user.is_active)
            # messages.add_message(request,messages.ERROR,"User Not Found you haved to Register First")
            return redirect("dologin")
       
        # return HttpResponseRedirect(reverse("patientregisterstep1",kwargs={'user_id':user.id}))
        # return HttpResponseRedirect(reverse("dologin"))

def dologin(request):
    if request.method == "POST":
    #check user is authenticate or not
        user=EmailBackEnd.authenticate(request,username=request.POST.get("username"),password=request.POST.get("password"))
        if user is not None:
            if user.is_active == True:
                login(request,user)
                next =request.POST.get('next')
                print("before check if")
                # request.session['logged in']=True
                if user.user_type=="2":
                    print("2")
                    if next:
                        return HttpResponseRedirect(next)
                    else:
                        return HttpResponseRedirect(reverse('admin:index'))
                if user.user_type=="4":
                    print("4")
                    if next:
                        return HttpResponseRedirect(next)
                    else:
                        return HttpResponseRedirect(reverse('home'))
                elif user.user_type=="1":
                    print("1")
                    if next:
                        return HttpResponseRedirect(next)
                    else:
                        return HttpResponseRedirect(reverse('admin_home'))
                elif user.user_type=="3":
                    print("3")
                    print(next)
                    if 'next' in request.POST:
                        return redirect(request.POST.get('next'))
                    else:
                        return HttpResponseRedirect(reverse('home'))
                else:
   # For Djnago default Admin Login return HttpResponseRedirect(reverse('admin:index'))
                    return HttpResponseRedirect(reverse('admin:index'))
            else:
                print("insdide else")
                messages.add_message(request,messages.ERROR,"Please Verify Your Account First")
                return redirect('/accounts/dologin')
        else:
            print("last else")
            # print(user.is_active)
            messages.add_message(request,messages.ERROR,"User Not Found you haved to Register First")
            return redirect("dologin")
    return render(request,'accounts/dologin.html')

class dosingup(SuccessMessageMixin,CreateView):
    template_name="accounts/dosingup.html"
    model=CustomUser
    fields=["email","phone","password"]
  
    def form_valid(self,form):

        #Saving Custom User Object for Merchant User
        user=form.save(commit=False)
        user.is_active=True
        user.user_type=3
        user.username= form.cleaned_data["phone"]
        user.set_password(form.cleaned_data["password"])
        user.counter += 1  # Update Counter At every Call
        user.save() # Save the data
        mobile= user.phone
        key = send_otp(mobile)
        user.otp = str(key)
        user.save()
        messages.add_message(self.request,messages.SUCCESS,"OTP has been sent successfully") 
        return HttpResponseRedirect(reverse("verifyPhone",kwargs={'phone':user.phone}))
        #Saving Merchant user
        # profile_pic=self.request.FILES["profile_pic"]
        # fs=FileSystemStorage()
        # filename=fs.save(profile_pic.name,profile_pic)
        # profile_pic_url=fs.url(filename)

        # user.customers.profile_pic=profile_pic_url
        # user.save()
        # messages.success(self.request,"Customer User Created")
        # return HttpResponseRedirect(reverse("dologin"))

class AuthorizedSingup(SuccessMessageMixin,CreateView):
    template_name="accounts/athorizationsnew.html"
    model=CustomUser
    fields=["email","phone","password"]
    success_message = "Admin User Created" 

    def form_valid(self,form):
        #Saving Custom User Object for Merchant User
        print('i m here at Hospital singup')
        user=form.save(commit=False)
        user.user_type=1
        user.is_active=True
        user.username = form.cleaned_data["phone"]
        user.set_password(form.cleaned_data["password"])
        print('just one step ahead save?')   
        user.save() # Save the data
        return HttpResponseRedirect(reverse("dologin"))
 

def dosingup1(request):
    if request.method=="POST":
        username = request.POST.get('username')
        r=CustomUser.objects.filter(username=username)
        if r.count():            
            messages.add_message(request,messages.ERROR,"Username  Already Exits")
            return HttpResponseRedirect(reverse("dosingup"))
        email = request.POST.get('email')
        e=CustomUser.objects.filter(email=email)
        if e.count():        
            messages.add_message(request,messages.ERROR,"Email Already Exits")
            return HttpResponseRedirect(reverse("dosingup"))
            
        phone = request.POST.get('phone')
        p=CustomUser.objects.filter(phone=phone)
        if p.count():
            messages.add_message(request,messages.ERROR,"Phone Already Exits")
            return HttpResponseRedirect(reverse("dosingup"))
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 and password2 and password1 != password2:
            messages.add_message(request,messages.ERROR,"Password Does Match")
            return HttpResponseRedirect(reverse("dosingup"))

        try:
            user=CustomUser.objects.create_user(username=username,password=password1,email=email)
            user.save(commit=False)
            user.phone=phone
            user.user_type="3"
            print(user,username,password1,email,phone)
            user.save()
            # current_site=get_current_site(request)
            # email_subject='Active your Account',
            # message=render_to_string('accounts/activate.html',
            # {
            #     'user':user,
            #     'domain':current_site.domain,
            #     'uid':urlsafe_base64_encode(force_bytes(user.pk/tt)),
            #     'token':generate_token.make_token(user)
            # }
            # )
            # print(urlsafe_base64_encode(force_bytes(user.pk)),)
            # print(generate_token.make_token(user))
            # print(current_site.domain)
            # email_message=EmailMessage(
            #     email_subject,
            #     message,
            #     settings.EMAIL_HOST_USER,
            #     [email]
            # )
            # email_message.send()
            # messages.add_message(request,messages.ERROR,"Sucessfully Singup Please Verify Your Account First")
            print("hello bhia ahiya ayo em")           
            return HttpResponseRedirect(reverse("dologin"))
        except:
            messages.add_message(request,messages.ERROR,"Connection Error Try Again")
            return HttpResponseRedirect(reverse("dosingup"))
    return render(request,"accounts/dosingup.html")

def customer_singup(request): 
    if request.method=="POST":
        username=request.POST.get('username')
        r=CustomUser.objects.filter(username=username)
        if r.count():
            messages.add_message(request,messages.ERROR,"Username  Already Exits")
            return HttpResponseRedirect(reverse("customer_singup"))

        email = request.POST.get('email')
        e=CustomUser.objects.filter(email=email)
        if e.count():
            if e.user_type==3:
                messages.add_message(request,messages.ERROR,"Email Already Exits")
                return HttpResponseRedirect(reverse("customer_singup"))
            else:
                messages.add_message(request,messages.ERROR,"Register With different Role")
                return HttpResponseRedirect(reverse("customer_singup"))

        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 and password2 and password1 != password2:
            messages.add_message(request,messages.ERROR,"Password Does Match")
            return HttpResponseRedirect(reverse("customer_singup"))
        try:
            user=CustomUser.objects.create_user(username=username,password=password1,email=email,user_type=3)
            user.is_active=True
            user.save()
            current_site=get_current_site(request)
            email_subject='Active your Account',
            message=render_to_string('accounts/activate.html',
            {
                'user':user,
                'domain':current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':generate_token.make_token(user)
            }
            )
            print(message)
            email_message=EmailMessage(
                email_subject,
                message,
                settings.EMAIL_HOST_USER,
                [email]
            )
            email_message.send()
            messages.add_message(request,messages.ERROR,"Sucessfully Singup check you emial for verification")
            return HttpResponseRedirect(reverse("dologin"))
        except:
            messages.add_message(request,messages.ERROR,"Connection Error Try Again")
            return HttpResponseRedirect(reverse("customer_singup"))
    return render(request,"accounts/customer_singup.html")

def activate(request,uidb64,token):
    try:
        uid=force_str(urlsafe_base64_decode(uidb64))
        print(uid)
        user=CustomUser.objects.get(pk=uid) 
    except:
        user=None
    if user is not None and generate_token.check_token(user,token):
        user.is_active=True
        user.save()
        messages.add_message(request,messages.SUCCESS,'account  is Activated Successfully')
        return redirect('/accounts/dologin')
    return render(request,'accounts/activate_failed.html',status=401)


