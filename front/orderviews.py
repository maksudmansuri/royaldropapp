from decimal import Decimal
from front.basket import Basket
from django.http import response
from accounts import admin
from accounts import models
from front.models import OrderTacker, Orders, Product, ProductChildSubCategory, ProductDetails,Product_Session,ProductCategory,ProductSubCategory,Product_Modules,productMedia
from accounts.EmailBackEnd import EmailBackEnd
from accounts.models import CustomUser, CustomersAddress, Staffs, Customers as Customers
from django.views.generic import ListView,CreateView,UpdateView,DetailView,View
from django.urls import reverse
from django.contrib import messages
from django.http.response import HttpResponse, HttpResponseRedirect
from django.contrib.auth import login,authenticate,logout
from django.shortcuts import get_object_or_404, render , redirect
from django.contrib.messages.views import SuccessMessageMixin
from accounts.forms import RegistrationForm
import json


class dashboardView(DetailView):
    def get(self,request,*args,**kwargs):
        customer = Customers.objects.get(admin=request.user.id)
        return render(request,"dashboard.html",{"customer":customer})

class dashMyProfileView(DetailView):
    def get(self,request,*args,**kwargs):
        customer = Customers.objects.get(admin=request.user.id)
        return render(request,"dash_my_profile.html",{"customer":customer})

class dashEditProfileUpdateView(UpdateView):
    def get(self,request,*args,**kwargs):
        customer = Customers.objects.get(admin=request.user.id)
        return render(request,"dash_edit_profile.html",{"customer":customer})
    
    def post(self,request,*args,**kwargs):        
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        gender=request.POST.get("gender")
        dob=request.POST.get("dob")
        print(first_name,last_name,gender)

        try:
            # user_id=kwargs["customers_id"]
            customer = Customers.objects.get(admin=request.user.id)
            customer.fisrt_name = first_name
            customer.last_name= last_name   
            customer.gender = gender
            customer.dob = dob
            customer.save()

            customer.admin.first_name = first_name
            customer.admin.last_name = last_name
            customer.admin.save()

            messages.success(self.request,"Product Updated Succesfully")
            # return HttpResponse("error in connection")
            return HttpResponseRedirect(reverse("dash_my_profile"))
        except:
            msg=messages.error(request,"Connection Error Try Again")
            # return HttpResponse("error in connection")
            return HttpResponseRedirect(reverse("dash_my_profile"))
 
class dashAddressBookView(ListView):
    def get(self,request,*args,**kwargs):
        customer = Customers.objects.get(admin=request.user.id)
        address = CustomersAddress.objects.filter(customer=customer)
        param = {"customer":customer,"address":address,}
        print("WE ARE HERE IN DASH ADDRESS BOOK VIEW")
        return render(request,"dash_address_book.html",param)

class dashAddressMakeDefaultView(DetailView):
    def get(self,request,*args,**kwargs):
        customer = Customers.objects.get(admin=request.user.id)
        address = CustomersAddress.objects.filter(customer=customer)
        param = {"customer":customer,"address":address,}
        return render(request,"dash_address_make_default.html",param)
 
    def post(self,request,*args,**kwargs):
        adds= request.POST.get("address")
        customer = Customers.objects.get(admin=request.user.id)
        is_default_address = CustomersAddress.objects.get(is_default=True,customer=customer)
        is_default_address.is_active= False
        is_default_address.is_default= False
        is_default_address.save()
        addresss = CustomersAddress.objects.filter(customer=customer)
        
        if adds == is_default_address.id:
            is_default_address.is_active= True
            is_default_address.is_default= True
            msg=messages.success(self.request,"same adress updated")           
            param = {"customer":customer,"address":addresss,}
            return render(request,"dash_address_make_default.html",param)
        try:           
            addresses = CustomersAddress.objects.get(id=adds)
            addresses.is_active= True
            addresses.is_default= True
            addresses.save()
            customer.fisrt_name = addresses.fisrt_name
            customer.last_name =addresses.last_name
            customer.address =addresses.address
            customer.city = addresses.city
            customer.state = addresses.state
            customer.country = addresses.country
            customer.zip_Code = addresses.zip_Code
            customer.phone =addresses.phone
            customer.save()
 
            msg=messages.success(self.request,"Default Address Updated Succesfully")
            param = {"customer":customer,"address":addresss,}
            return render(request,"dash_address_book.html",param)
        except:
            msg=messages.error(request,"Connection Error Try Again")            
            return HttpResponseRedirect(reverse("dash_address_make_default"))

class dashAddressAddView(SuccessMessageMixin,CreateView):   
    def get(self, request, *args, **kwargs):
        customer =  Customers.objects.get(admin=request.user.id)
        address = CustomersAddress.objects.filter(customer=customer)
        param = {"customer":customer,"address":address}
        return render(request,"dash_address_add.html",param)

    def post(self,request,*args,**kwargs):
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        address=request.POST.get("address")
        city=request.POST.get("city")
        state=request.POST.get("state")
        country=request.POST.get("country")
        zip_Code=request.POST.get("zip_Code")
        phone=request.POST.get("phone")
        try:
            customer = Customers.objects.get(admin=request.user.id)
            add = CustomersAddress.objects.filter(customer=customer)
            print(customer,add)            
            if customer.address and add:
                addresss = CustomersAddress(customer=customer,fisrt_name=first_name,last_name=last_name,address=address,city=city,state=state,country=country,phone=phone,zip_Code=zip_Code)
                addresss.is_active = False
                addresss.is_default = False
                addresss.save()
            else:
                customer.fisrt_name = first_name
                customer.last_name =last_name
                customer.address =address
                customer.city = city  
                customer.state = state
                customer.country = country
                customer.zip_Code = zip_Code
                customer.phone =phone
                customer.save()
                print("we are after customer save")
                addresss = CustomersAddress(customer=customer,fisrt_name=first_name,last_name=last_name,address=address,city=city,state=state,country=country,phone=phone,zip_Code=zip_Code)
                addresss.is_active = True
                addresss.is_default = True
                addresss.save()
            msg=messages.success(self.request,"Product Created Succesfully")
            return HttpResponseRedirect(reverse("dash_address_book"))
            # return HttpResponse("Ok")
        except:
            msg=messages.error(request,"Connection Error Try Again")
            # return HttpResponse("error in connection")
            return HttpResponseRedirect(reverse("dash_address_book"))

class checoutAddressAddView(SuccessMessageMixin,CreateView):
    def post(self,request,*args,**kwargs):
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        username = first_name + last_name
        address1=request.POST.get("address")
        address2=request.POST.get("address2")
        city=request.POST.get("city")
        state=request.POST.get("state")
        country=request.POST.get("country")
        zip_Code=request.POST.get("zip_Code")
        phone=request.POST.get("phone")
        is_default=request.POST.get("is_default")
        print(is_default)
        address= address1 + address2

        try:
            customer = Customers.objects.get(admin=request.user.id)            
            if customer.address:
                is_active_address = CustomersAddress.objects.get(customer=customer,is_active=True)
                is_active_address.is_active = False
                is_active_address.save()
                addresss = CustomersAddress(customer=customer,fisrt_name=first_name,last_name=last_name,address=address,city=city,state=state,country=country,phone=phone,zip_Code=zip_Code)
                addresss.is_active = True
                addresss.is_default = False
                if is_default == "on":       
                    is_default_address = CustomersAddress.objects.get(customer=customer,is_default=True)
                    is_default_address.is_default = False
                    is_default_address.save()            
                    addresss.is_active = True
                    addresss.is_default = True
                    customer.fisrt_name = first_name
                    customer.last_name =last_name
                    customer.address =address
                    customer.city = city  
                    customer.state = state
                    customer.country = country
                    customer.zip_Code = zip_Code
                    customer.phone =phone
                    customer.save() 
                addresss.save()
            else:
                customer.fisrt_name = first_name
                customer.last_name =last_name
                customer.address =address
                customer.city = city  
                customer.state = state
                customer.country = country
                customer.zip_Code = zip_Code
                customer.phone =phone
                customer.save() 
                addresss = CustomersAddress(customer=customer,fisrt_name=first_name,last_name=last_name,address=address,city=city,state=state,country=country,phone=phone,zip_Code=zip_Code)
                addresss.is_active = True
                addresss.is_default = True
                # if is_default == "on":
                #     addresss.is_active = 1
                addresss.save()
            
                
            msg=messages.success(self.request,"Product Created Succesfully")
            return HttpResponseRedirect(reverse("checkout"))
            # return HttpResponse("Ok")
        except:
            msg=messages.error(request,"Connection Error Try Again")
            # return HttpResponse("error in connection")
            return HttpResponseRedirect(reverse("checkout"))

class dashAddressUpdateView(SuccessMessageMixin,UpdateView):
    model = CustomersAddress
    fields = "__all__"
    template_name="dash_address_edit.html"

    def post(self,request,*args,**kwargs):
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        address=request.POST.get("address")
        city=request.POST.get("city")
        state=request.POST.get("state")
        country=request.POST.get("country")
        zip_Code=request.POST.get("zip_Code")
        phone=request.POST.get("phone")
       
        address_id = kwargs["pk"]
        customer = Customers.objects.get(admin=request.user.id)
        addresss = CustomersAddress.objects.get(id=address_id)
        addresss.customer=customer
        addresss.fisrt_name=first_name
        addresss.last_name=last_name
        addresss.address=address
        addresss.city=city
        addresss.state=state
        addresss.country=country
        addresss.phone=phone
        addresss.zip_Code=zip_Code
        addresss.save()
        
        return HttpResponseRedirect(reverse("dash_address_book"))

class dashTrackOrderByTrackerView(DetailView):
    def get(self,request,*args,**kwargs):
        customer = Customers.objects.get(admin=request.user.id)
        return render(request,"dash_manage_order.html.html",{"customer":customer})

class dashTrackOrderView(DetailView):
    def get(self,request,*args,**kwargs):
        customer = Customers.objects.get(admin=request.user.id)
        return render(request,"dash_track_order.html",{"customer":customer})

    def post(self,request,*args, **kwargs):
        email=request.POST.get('email')
        ordes_id=request.POST.get('order_id')
        print("i m here")
        try:
            if email == request.user.email:
                order = Orders.objects.get(id=ordes_id)
                if order:
                    update = OrderTacker.objects.filter(ordes_id=ordes_id)
                    updates = []
                    for item in update:
                        updates.append({'id':item.id,'text':item.desc,'time':item.created_date})
                        response = json.dumps([updates,order.product_Json,order.address.fisrt_name,order.address.last_name,order.address.address,order.address.city,order.address.state,order.address.country,order.address.zip_Code,order.address.phone ,order.payment_method],default=str)
                    print(response)
                    return HttpResponse(response)
                else:
                    return HttpResponse('{}')
            else:
                return HttpResponse('{}')
        except Exception as e:
            return HttpResponse('{}')
        # return render(request,"dash_track_order.html")
        # messages.add_message(request,messages.ERROR,'Email id or Order can not be match !')
        # return HttpResponseRedirect(reverse("dash_track_order"))


class dashManageOrderView(DetailView):
    def get(self,request,*args,**kwargs):
        customer = Customers.objects.get(admin=request.user.id)
        param = {"customer":customer}
        return render(request,"dash_manage_order.html",param)

class dashMyOrderView(DetailView):
    def get(self,request,*args,**kwargs):
        try:
            customer = Customers.objects.get(admin=request.user.id)
            orders = Orders.objects.filter(customer = customer)
            # jsonvalue =Orders.objects.select_related().values('product_Json').filter(customer = customer)
            # response = json.dumps(jsonvalue,default=str)
            context = {"orders":orders}
            return render(request,"dash_my_order.html",context)
        except Exception as e:
            return HttpResponse(e)

class dashMyOrderDetailView(DetailView):
    def get(self,request,*args,**kwargs):
        try:
            customer = Customers.objects.get(admin=request.user.id)
            orders = Orders.objects.filter(customer = customer)
            print(orders)
            jsonvalues =Orders.objects.select_related().values('product_Json').filter(customer = customer)
            # for jsonvalue in jsonvalues:
            #     response = json.dumps(jsonvalue,default=str)
            return HttpResponse(jsonvalues)
        except Exception as e:
            return HttpResponse(e)


class dashPaymentOptionView(DetailView):
    def get(self,request,*args,**kwargs):
        customer = Customers.objects.get(admin=request.user.id)
        return render(request,"dash_payment_option.html",{"customer":customer})
 
class dashCancellationView(DetailView):
    def get(self,request,*args,**kwargs):
        customer = Customers.objects.get(admin=request.user.id)
        return render(request,"dash_cancellation.html",{"customer":customer})

class checkoutDefaultAddresschangeView(View):
    def post(self,request,*args,**kwargs):
        adds= request.POST.get("default-address")
        customer = Customers.objects.get(admin=request.user.id)
        is_default_address = CustomersAddress.objects.get(is_default=True,customer=customer)
        is_default_address.is_default= False
        is_default_address.save()
        is_active_address = CustomersAddress.objects.get(is_active=True,customer=customer)
        is_active_address.is_active= False
        is_active_address.save()

        addresss = CustomersAddress.objects.filter(customer=customer)
        
        if adds == is_default_address.id:
            is_default_address.is_active= True
            is_default_address.is_default= True
            msg=messages.success(self.request,"same adress updated")           
            param = {"customer":customer,"address":addresss,}
            return HttpResponseRedirect(reverse("checkout"))
        try:           
            addresses = CustomersAddress.objects.get(id=adds)
            addresses.is_active= True
            addresses.is_default= True
            addresses.save()
            customer.fisrt_name = addresses.fisrt_name
            customer.last_name =addresses.last_name
            customer.address =addresses.address
            customer.city = addresses.city
            customer.state = addresses.state
            customer.country = addresses.country
            customer.zip_Code = addresses.zip_Code
            customer.phone =addresses.phone
            customer.save()
 
            msg=messages.success(self.request,"Default Address Updated Succesfully")
            return HttpResponseRedirect(reverse("checkout"))
        except:
            msg=messages.error(request,"Connection Error Try Again")            
            return HttpResponseRedirect(reverse("checkout"))
    

class CheckoutListView(View):
    def get(self, request, *args, **kwargs):
        product = Product.objects.filter(is_active=True)
        customer = Customers.objects.get(admin=request.user.id)
        address = CustomersAddress.objects.filter(customer=customer)

        is_active_address = CustomersAddress.objects.get(customer=customer,is_active=True)
        is_default_address = CustomersAddress.objects.get(customer=customer,is_default=True)
        param = {"product":product,"customer":customer,"address":address,"is_active_address":is_active_address,"is_default_address":is_default_address}      
        return render(request,"checkout.html",param)

    def post(self,request,*args, **kwargs):
        basket = Basket(request)
        paymet_method = request.POST.get("payment") 
        amount = basket.get_total_price()
        print(amount)
        product_Json = request.POST.get("product_Json")
        try:
            customer = Customers.objects.get(admin=request.user.id)
            is_active_address = CustomersAddress.objects.get(customer=customer,is_active=True)
            order = Orders(payment_method=paymet_method,customer=customer,product_Json=product_Json,amount=amount)
            order.address = is_active_address
            order.save()
            print("order save")

            tracker = OrderTacker(ordes_id=order.id,desc="product purchase successfuly !")
            tracker.save()

            thank =True
            if thank:
                param = {'thank':thank}
                return render(request,"checkout.html",param)
            else:
                return HttpResponseRedirect(reverse("dash_manage_order"))
        except:
            msg=messages.error(request,"Connection Error Try Again")
            # return HttpResponse("error in connection")
            return HttpResponseRedirect(reverse("checkout"))

    
    
    # def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:

    #     return super().get(request, *args, **kwargs)
