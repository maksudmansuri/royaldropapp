# from django.shortcuts import render,redirect
# from django.http import HttpResponse
# from .forms import UserCreationForm
# from django.contrib import messages
# from .models import UserDetail

# Create your views here.
# def index(request):
#     # if request.user.is_superuser:
# 	# 	return redirect('admin2')
# 	# elif request.user.is_staff:
# 	# 	return redirect("saler_home")
# 	# else:
# 		pass
#     # return HttpResponse("index page ")


from django.shortcuts import render
from django.http import HttpResponse
import http.client
# Create your views here.
import json
import requests
import ast

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status, generics
# from forms import UserForm
from .models import User, PhoneOTP
from django.shortcuts import get_object_or_404, redirect
import random
from .serializer import CreateUserSerializer, LoginSerializer
from knox.views import LoginView as KnoxLoginView
from knox.auth import TokenAuthentication
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth import login,logout

conn = http.client.HTTPConnection("2factor.in")


class ValidatePhoneSendOTP(APIView):

    def post(self, request, *args, **kwargs):
        phone_number = request.data.get('phone')
        password = request.data.get('password', False)
        username = request.data.get('username', False)
        email    = request.data.get('email', False)

        if phone_number:
            phone = str(phone_number)
            user = User.objects.filter(phone__iexact = phone)
            if user.exists():
                return Response({
                    'status' : False,
                    'detail' : 'Phone number already exists'
                })

            else:
                key = send_otp(phone)
                if key:
                    old = PhoneOTP.objects.filter(phone__iexact = phone)
                    if old.exists():
                        old = old.first()
                        count = old.count
                        if count > 10:
                            return Response({
                                'status' : False,
                                'detail' : 'Sending otp error. Limit Exceeded. Please Contact Customer support'
                            })

                        old.count = count +1
                        old.save()
                        print('Count Increase', count)

                        conn.request("GET", "https://2factor.in/API/V1/f08f2dc9-aa1a-11eb-80ea-0200cd936042/SMS/"+phone+"/"+str(key))

                        # conn.request("GET", "https://2factor.in/API/R1/?module=SMS_OTP&apikey=f08f2dc9-aa1a-11eb-80ea-0200cd936042"+phone+"&otpvalue="+str(key)+"&templatename=WomenMark1")
                        # conn.request("GET", "http://dnd.saakshisoftware.in/api/mt/SendSMS?user=Sect&password=Sect@123&senderid=GLOBAL&channel=Promo&DCS=0&flashsms=0&number=91989xxxxxxx&text=test message&route=##&DLTTemplateId=approvded dlt templateid&PEID=sender entity id")
                        res = conn.getresponse() 
                       
                        data = res.read()
                        data=data.decode("utf-8")
                        data=ast.literal_eval(data)
                        
                        
                        if data["Status"] == 'Success':
                            old.otp_session_id = data["Details"]
                            old.save()
                            print('In validate phone :'+old.otp_session_id)
                            return Response({
                                   'status' : True,
                                   'detail' : 'OTP sent successfully'
                                })    
                        else:
                            return Response({
                                  'status' : False,
                                  'detail' : 'OTP sending Failed'
                                }) 

                       


                    else:

                        obj=PhoneOTP.objects.create(
                            phone=phone,
                            otp = key,
                            email=email,
                            username=username,
                            password=password,
                        )
                        conn.request("GET", "https://2factor.in/API/V1/f08f2dc9-aa1a-11eb-80ea-0200cd936042/SMS/"+phone+"/"+str(key))
                        res = conn.getresponse()    
                        data = res.read()
                        print(data.decode("utf-8"))
                        data=data.decode("utf-8")
                        data=ast.literal_eval(data)

                        if data["Status"] == 'Success':
                            obj.otp_session_id = data["Details"]
                            obj.save()
                            print('In validate phone :'+obj.otp_session_id)
                            return Response({
                                   'status' : True,
                                   'detail' : 'OTP sent successfully'
                                })    
                        else:
                            return Response({
                                  'status' : False,
                                  'detail' : 'OTP sending Failed'
                                })

                        
                else:
                     return Response({
                           'status' : False,
                            'detail' : 'Sending otp error'
                     })   

        else:
            return Response({
                'status' : False,
                'detail' : 'Phone number is not given in post request'
            })            

def send_otp(phone):
    if phone:
        key = random.randint(999,9999)
        print(key)
        return key
    else:
        return False

class ValidateOTP(APIView):

    def post(self, request, *args, **kwargs):
        phone = request.data.get('phone', False)
        otp_sent = request.data.get('otp', False)


        if phone and otp_sent:
            old = PhoneOTP.objects.filter(phone__iexact = phone)
            if old.exists():
                old = old.first()
                otp_session_id = old.otp_session_id
                print("In validate otp"+otp_session_id)
                conn.request("GET", "http://2factor.in/API/V1/f08f2dc9-aa1a-11eb-80ea-0200cd936042/SMS/VERIFY/"+otp_session_id+"/"+otp_sent)
                res = conn.getresponse()    
                data = res.read()
                print(data.decode("utf-8"))
                data=data.decode("utf-8")
                data=ast.literal_eval(data)
                
                

                if data["Status"] == 'Success':
                    old.validated = True
                    old.save()
                    return Response({
                        'status' : True,
                        'detail' : 'OTP MATCHED. Please proceed for registration.'
                            })

                else:
                    return Response({
                        'status' : False,
                        'detail' : 'OTP INCORRECT'
                    })
                


            else:
                return Response({
                        'status' : False,
                        'detail' : 'First Proceed via sending otp request'
                    })


        else:
            return Response({
                        'status' : False,
                        'detail' : 'Please provide both phone and otp for Validation'
                    })

class Register(APIView):

    def post(self, request, *args, **kwargs):
        phone = request.data.get('phone', False)
        password = request.data.get('password', False)
        username = request.data.get('username', False)
        email    = request.data.get('email', False)


        if phone and password and username and email :
            old = PhoneOTP.objects.filter(phone__iexact = phone)
            if old.exists():
                old = old.first()
                validated = old.validated

                if validated:
                        temp_data = {
                            'username' : old.username,
                            'email' : old.email,
                            'phone' : old.phone,
                            'password' : old.password,
                         
                        }
                        serializer = CreateUserSerializer(data = temp_data)
                        serializer.is_valid(raise_exception = True)
                        user = serializer.save()
                        user.set_password(old.password)
                        user.save()
                        print(user)
                        print(old.password)
                        old.delete()
                        return Response({
                            'status' : True,
                            'detail' : 'Account Created Successfully'
                            })   

                else:
                    return Response({
                        'status' : False,
                        'detail' : 'OTP havent Verified. First do that Step.'
                        })


            else:    
                return Response({
                'status' : False,
                'detail' : 'Please verify Phone First'
            })   
        else:
            return Response({
                'status' : False,
                'detail' : 'Enter All Require Fields'
            })  

class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny, )

    def post(self, request, format = None):
        serializer = LoginSerializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        user = serializer.validated_data['user']
        login(request, user)
        return super().post(request, format=None)




# # def register(request):
#     if request.user.is_authenticated:
# 	# 	return redirect('home')
#         return HttpResponse("index page ")
#     else:
#         if request == "POST":
#             if request.method == 'POST':
#                 form = UserRegisterForm(request.POST)
#                 if form.is_valid():
#                     form.save()
#                     username = form.cleaned_data.get('username')
#                     usr = User.objects.filter(username=username).first()
#                     if username.isdigit():
#                         UserDetail(user=usr,mobile=username).save()
#                     else:
#                         usr.email = username
#                         usr.save()
#                         UserDetail(user=usr).save()
#                     messages.success(request, f'Account is Created for {username}')
#                     return redirect('login')
#             else:
#                 form = UserRegisterForm()
#     return render(request, 'accounts/signup.html', {'form':form})
#     #  'title':'Sign Up',})
#     # 'category':category.objects.all()})[]