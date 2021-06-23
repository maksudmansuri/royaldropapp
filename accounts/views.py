from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render,redirect,HttpResponseRedirect
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
from django.utils.encoding import force_bytes,force_text,DjangoUnicodeDecodeError
from .utils import generate_token
from django.core.mail import EmailMessage
from django.conf import settings
from rest_framework import viewsets
from django.core.files.storage import FileSystemStorage

#API for Apps
# class CustomUserViewSet(viewsets.ModelViewSet):
#     queryset = CustomUser.objects.all().order_by('username')
#     serializer_class = CustomUserSerializer
 

# Create your views here .gg

# def soc_login(request):
#     return render(request,'dologin')

def dologin(request):
    print(request.user)
    if request.method == "POST":
    #check user is authenticate or not
        user=EmailBackEnd.authenticate(request,username=request.POST.get("username"),password=request.POST.get("password"))
        if user is not None:
            if user.is_active == True:
                print(user.is_active)
                login(request,user)
                # request.session['logged in']=True
                if user.user_type=="4":
                    return HttpResponseRedirect(reverse('admin_home'))
                elif user.user_type=="2":
                    return HttpResponseRedirect(reverse('admin_home'))
                elif user.user_type=="3":
                    if 'next' in request.POST:
                        return redirect(request.POST.get('next'))
                    else:
                        return HttpResponseRedirect(reverse('home'))
                else:
   # For Djnago default Admin Login return HttpResponseRedirect(reverse('admin:index'))
                    return HttpResponseRedirect(reverse('admin_home'))

            else:
                messages.add_message(request,messages.ERROR,"Please Verify Your Account First")
                return redirect('/accounts/dologin')
        else:
            # print(user.is_active)
            messages.add_message(request,messages.ERROR,"User Not Found you haved to Register First")
            return redirect("dologin")
    return render(request,'accounts/dologin.html')
       
class dosingup(SuccessMessageMixin,CreateView):
    template_name="accounts/dosingup.html"
    model=CustomUser
    fields=["email","phone","username","password"]
  
    def form_valid(self,form):

        #Saving Custom User Object for Merchant User
        user=form.save(commit=False)
        user.is_active=True
        user.user_type=3
        user.set_password(form.cleaned_data["password"])
        user.save()

        #Saving Merchant user
        # profile_pic=self.request.FILES["profile_pic"]
        # fs=FileSystemStorage()
        # filename=fs.save(profile_pic.name,profile_pic)
        # profile_pic_url=fs.url(filename)

        # user.customers.profile_pic=profile_pic_url
        # user.save()
        messages.success(self.request,"Customer User Created")
        return HttpResponseRedirect(reverse("dologin"))

def dosingup1(request):
    if request.method=="POST":
        username = request.POST.get('username')
        r=CustomUser.objects.filter(username=username)
        if r.count():
            msg=messages.error(request,"Username  Already Exits")
            return HttpResponseRedirect(reverse("dosingup"))

        email = request.POST.get('email')
        e=CustomUser.objects.filter(email=email)
        if e.count():        
            msg=messages.error(request,"Email Already Exits")
            return HttpResponseRedirect(reverse("dosingup"))
            
        phone = request.POST.get('phone')
        p=CustomUser.objects.filter(phone=phone)
        if p.count():
            msg=messages.error(request,"Phone Already Exits")
            return HttpResponseRedirect(reverse("dosingup"))
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 and password2 and password1 != password2:
            msg=messages.error(request,"Password Does Match")
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
            # msg=messages.success(request,"Sucessfully Singup Please Verify Your Account First")
            print("hello bhia ahiya ayo em")           
            return HttpResponseRedirect(reverse("dologin"))
        except:
            msg=messages.error(request,"Connection Error Try Again")
            return HttpResponseRedirect(reverse("dosingup"))
    return render(request,"accounts/dosingup.html")


def instructor_singup(request):
    if request.method=="POST":
        username = request.POST.get('username')
        r=CustomUser.objects.filter(username=username)
        if r.count():
            msg=messages.error(request,"Username  Already Exits")
            return HttpResponseRedirect(reverse("instructor_singup"))

        email = request.POST.get('email')
        e=CustomUser.objects.filter(email=email)
        if e.count():
            if e.user_type==2:
                msg=messages.error(request,"Email Already Exits")
                return HttpResponseRedirect(reverse("instructor_singup"))
            else:
                msg=messages.error(request,"Register with Other Accounts")
                return HttpResponseRedirect(reverse("instructor_singup"))
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 and password2 and password1 != password2:
            msg=messages.error(request,"Password Does Match")
            return HttpResponseRedirect(reverse("instructor_singup"))

        try:
            user=CustomUser.objects.create_user(username=username,password=password1,email=email)
            user.user_type="2"
            user.is_active=True
            print(user,username,password1,email)
            user.save()
            # current_site=get_current_site(request)
            # email_subject='Active your Account',
            # message=render_to_string('accounts/activate.html',
            # {
            #     'user':user,
            #     'domain':current_site.domain,
            #     'uid':urlsafe_base64_encode(force_bytes(user.pk)),
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
            # msg=messages.success(request,"Sucessfully Singup Please Verify Your Account First")
            return HttpResponseRedirect(reverse("dologin"))
        except:
            msg=messages.error(request,"Connection Error Try Again")
            return HttpResponseRedirect(reverse("instructor_singup"))
    return render(request,"accounts/instructor_singup.html")

def customer_singup(request): 
    if request.method=="POST":
        username=request.POST.get('username')
        r=CustomUser.objects.filter(username=username)
        if r.count():
            msg=messages.error(request,"Username  Already Exits")
            return HttpResponseRedirect(reverse("customer_singup"))

        email = request.POST.get('email')
        e=CustomUser.objects.filter(email=email)
        if e.count():
            if e.user_type==3:
                msg=messages.error(request,"Email Already Exits")
                return HttpResponseRedirect(reverse("customer_singup"))
            else:
                msg=messages.error(request,"Register With different Role")
                return HttpResponseRedirect(reverse("customer_singup"))

        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 and password2 and password1 != password2:
            msg=messages.error(request,"Password Does Match")
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
            msg=messages.success(request,"Sucessfully Singup check you emial for verification")
            return HttpResponseRedirect(reverse("dologin"))
        except:
            msg=messages.error(request,"Connection Error Try Again")
            return HttpResponseRedirect(reverse("customer_singup"))
    return render(request,"accounts/customer_singup.html")

def counsellor_singup(request):
    if request.method=="POST":
        username=request.POST.get('username')
        email=request.POST.get('email')
        password=request.POST.get('password1')
        try: 
            user=CustomUser.objects.create_user(username=username,password=password,email=email,user_type=1)
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
            email_message=EmailMessage(
                email_subject,
                message,
                settings.EMAIL_HOST_USER,
                [email]
            )
            email_message.send()
            msg=messages.success(request,"Sucessfully Singup check you emial for verification")
            return HttpResponseRedirect(reverse("dologin"))
        except:
            msg=messages.error(request,"Connection Error Try Again")
            return HttpResponseRedirect(reverse("counsellor_singup"))
    return render(request,"accounts/counsellor_singup.html")

def selection(request):
    return render(request,"accounts/selection.html")

def activate(request,uidb64,token):
    try:
        uid=force_text(urlsafe_base64_decode(uidb64))
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


