from front.models import Product, ProductChildSubCategory, ProductDetails,Product_Session,ProductCategory,ProductSubCategory,Product_Modules, productMedia
from accounts.EmailBackEnd import EmailBackEnd
from accounts.models import CustomersAddress, Staffs, Customers as Customers
from django.views.generic import ListView,CreateView,UpdateView,DetailView,View
from django.urls import reverse
from django.contrib import messages
from django.http.response import HttpResponse, HttpResponseRedirect
from django.contrib.auth import login,authenticate,logout
from django.shortcuts import get_object_or_404, render , redirect
from django.contrib.messages.views import SuccessMessageMixin


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
        return render(request,"dash_address_book.html",param)

class dashAddressMakeDefaultView(DetailView):
    def get(self,request,*args,**kwargs):
        customer = Customers.objects.get(admin=request.user.id)
        address = CustomersAddress.objects.filter(customer=customer)
        param = {"customer":customer,"address":address,}
        return render(request,"dash_address_make_default.html",param)
 
    def post(self,request,*args,**kwargs):
        adds= request.POST.get("address_hide")
        print(adds)

        customer = Customers.objects.get(admin=request.user.id)
        # addresses = CustomersAddress.objects.filter(customer=customer)
        # add = [] 
        # for addres in addresses:
        #     adds= request.POST.getlist(addres.id)
        #     if adds.id == addres.id:
        #         customer.fisrt_name = addres.fisrt_name
        #         customer.last_name =addres.last_name
        #         customer.address =addres.address
        #         customer.city = addres.city
        #         customer.state = addres.state
        #         customer.country = addres.country
        #         customer.zip_Code = addres.zip_Code
        #         customer.phone =addres.phone
        #         customer.save()

        customer = Customers.objects.get(admin=request.user.id)
        address = CustomersAddress.objects.filter(customer=customer)
        param = {"customer":customer,"address":address,}
        return render(request,"dash_address_make_default.html",param)

class dashAddressAddView(SuccessMessageMixin,CreateView):
    model = CustomersAddress
    fields ="__all__"
    template_name="dash_address_add.html"

    def post(self,request,*args,**kwargs):
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        address=request.POST.get("address")
        city=request.POST.get("city")
        state=request.POST.get("state")
        country=request.POST.get("country")
        zip_Code=request.POST.get("zip_Code")
        phone=request.POST.get("phone")
       
        customer = Customers.objects.get(admin=request.user.id)
        if customer.address:
            addresss = CustomersAddress(customer=customer,fisrt_name=first_name,last_name=last_name,address=address,city=city,state=state,country=country,phone=phone,zip_Code=zip_Code)
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
            addresss.save()
        
        return HttpResponseRedirect(reverse("dash_address_book"))

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

class dashTrackOrderView(DetailView):
    def get(self,request,*args,**kwargs):
        customer = Customers.objects.get(admin=request.user.id)
        return render(request,"dashboard.html",{"customer":customer})

class dashMyOrderView(DetailView):
    def get(self,request,*args,**kwargs):
        customer = Customers.objects.get(admin=request.user.id)
        return render(request,"dashboard.html",{"customer":customer})

class dashPaymentOptionView(DetailView):
    def get(self,request,*args,**kwargs):
        customer = Customers.objects.get(admin=request.user.id)
        return render(request,"dashboard.html",{"customer":customer})

class dashCancellationView(DetailView):
    def get(self,request,*args,**kwargs):
        customer = Customers.objects.get(admin=request.user.id)
        return render(request,"dashboard.html",{"customer":customer})

class CheckoutListView(View):
    def get(self, request, *args, **kwargs):
        product = Product.objects.filter(is_active=True)
        customer = Customers.objects.get(admin=request.user.id)
        address = CustomersAddress.objects.filter(customer=customer)
        param = {"product":product,"customer":customer,"address":address}
        return render(request,"checkout.html",param)
    
 
    # def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:

    #     return super().get(request, *args, **kwargs)
  