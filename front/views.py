from datetime import datetime
from decimal import Decimal
from http.client import HTTPResponse
from django.shortcuts import render
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest
# authorize razorpay client with API Keys.
razorpay_client = razorpay.Client(
	auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
#end rozerpay import

from cart.helpers import CartHelper
from cart.models import Cart
from front import orderviews
from .basket import Basket
from django.shortcuts import get_object_or_404, render , redirect
# from django.views.generic.base import View
from .forms import RegisterForm
from django.contrib.auth import login,authenticate,logout
#from django.contrib.auth.models import User
from front.models import OrderTacker, Orders, Product, ProductChildSubCategory, ProductDetails,ProductCategory, ProductStockManage,ProductSubCategory,TempOrder, productGst, productMedia
from math import ceil
from accounts.EmailBackEnd import EmailBackEnd
from django.db.models import Q, fields
from django.core.paginator import Page,PageNotAnInteger,Paginator
from accounts.models import CustomersAddress, Staffs, Customers as Customers
from django.views.generic import ListView,CreateView,UpdateView,DetailView,View
from django import template
from django.urls import reverse
from django.contrib import messages
from django.http.response import HttpResponse, HttpResponseRedirect, JsonResponse
import json

from front import basket
register = template.Library()
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
# Create your vie ws here.v
 
#use it for url and its section inside same page
@register.simple_tag
def anchor(url_name, section_id):
    return reverse(url_name) + '#' + section_id

# class CategoriesListViews(ListView):
#     model = ProductCategory
#     tem_name = "front/category_list.html"

# class CategoriesCreateView(CreateView):
#     model = ProductCategory
#     fields = "__all__"
#     template_name = "front/categorycreate.html"

class indexView(ListView):
    model = Product
    fields ="__all__"
    template_name="index.html"
 
    def get(self,request,*args,**kwargs):
        product_list = []
        products=Product.objects.filter(is_active=1)
        n=len(products)
        nSlides=n//4 + ceil((n/4)-(n//4))
        params={'no_of_slides':nSlides,'range':range(nSlides),'product':products}
        productcategory = ProductCategory.objects.filter(is_active=1)
        productsubcategory = ProductSubCategory.objects.filter(is_active=1)
        productchildsubcategory = ProductChildSubCategory.objects.filter(is_active=1)
        for product in products:
            media=productMedia.objects.filter(product=product).first()
            product_list.append({"product":product,"media":media})
        return render(request,"index.html",{"productcategory":productcategory,"productsubcategory":productsubcategory,"products":product_list,'productchildsubcategory':productchildsubcategory})
    
# def index(request):
    # allProduct=[]
    # allcats=[]
    # allcrs=Product.objects.all()
    # allcrscnt=Product.objects.all().count()
    # allstfcnt=Staffs.objects.all().count()
    # allstdcnt=Customers.objects.all().count()
    # catProduct=Product.objects.values('product_category','id')
    # print(catProduct)
    # cats={item['product_category'] for item in catProduct}
    # for cat in cats:
    #     allcat=ProductCategory.objects.get(id=cat)
    #     crs=Product.objects.filter(product_category=cat,is_verified=True)
    #     n=len(crs)
    #     # nSlides=n/4+ceil((n/4)-(n//4))    
    #     allProduct.append([crs,range(1,n)])
    #     allcats.append(allcat)
    #     for i in crs:  
    #         print(i.Product_category)
 
    # print(allcats)
    # params= {'allProduct':allProduct,'allcats':allcats,'allcrscnt':allcrscnt,'allstfcnt':allstfcnt,'allstdcnt':allstdcnt,'allcrs':allcrs}
    # return render(request,'index.html')
 
class HomeListview(ListView):
    model = Product
    fields ="__all__"
    template_name="index2.html"
     
    def get_queryset(self):
        filter_val=self.request.GET.get("filter","")
        order_by=self.request.GET.get("orderby","id")
        if filter_val!="":
            product=Product.objects.filter(Q(product_name__contains=filter_val) | Q(product_brand__contains=filter_val) | Q(product_desc__contains=filter_val) | Q(product_l_desc__contains=filter_val) |Q(updated_at__contains=filter_val) ).order_by(order_by)
        else:
            product=Product.objects.all().order_by(order_by)

        return product
   
    def get_context_data(self,**kwargs):
        context=super(HomeListview,self).get_context_data(**kwargs)
        context["filter"]=self.request.GET.get("filter","")
        context["orderby"]=self.request.GET.get("orderby","id")
        context["all_table_fields"]=Product._meta.get_fields()
        return context
 
    def get(self,request,*args,**kwargs):
        caties = ProductCategory.objects.filter(is_active=True)
        subcaties = ProductSubCategory.objects.filter(is_active=True)
        childsubcaties = ProductChildSubCategory.objects.filter(is_active=True)
        exclusive_products = Product.objects.filter(is_active=True,is_exclusive = True)
        new_arrival_products = Product.objects.filter(is_active=True).order_by('-id')[:10][:10]
        
        allprods=[]
        catprods=Product.objects.values('product_category')
        subcatprod=Product.objects.values('product_subcategory')
        # print(subcatprods)
        # print(catprods)
        subcatprods = {item['product_subcategory'] for item in subcatprod}
        cats={item['product_category'] for item in catprods}
        prod =[]
        for cat in cats:
            filter_val=self.request.GET.get("filter","")
            order_by=self.request.GET.get("orderby","id")
            if filter_val!="":
                prods=Product.objects.filter(Q(product_name__contains=filter_val) | Q(product_brand__contains=filter_val) | Q(product_desc__contains=filter_val) | Q(product_l_desc__contains=filter_val) |Q(updated_at__contains=filter_val) ).order_by(order_by)
            else:
                prods=Product.objects.filter(product_category=cat,is_active=True).order_by(order_by)
            # prods = Product.objects.filter(product_category=cat,is_active=1)
            # print(prods)
            prod =[]
            for product in prods: 
                media=productMedia.objects.filter(product=product).first()
                product_stock=ProductStockManage.objects.get(product=product)
                prod.append({"product":product,"media":media,'product_stock':product_stock})            
            n=len(prod)
            # print(prod)
            nSlides=n//4 + ceil((n/4)-(n//4))
            productcategories = ProductCategory.objects.get(id=cat,is_active=1)
            # productsubcategories=[]
            # for productcategory in productcategories:
            #     productsubcategy = ProductSubCategory.objects.filter(category=productcategory,is_active=1)
            #     productsubcategories.append({productsubcategy})
            
            prodsub=ProductSubCategory.objects.filter(category=cat,is_active=1)
            allprods.append([prod,range(nSlides),nSlides,productcategories,prodsub])           
        params={'allprods':allprods,"cats":caties,"subcaties":subcaties,'childsubcaties':childsubcaties,'exclusive_products':exclusive_products,'new_arrival_products':new_arrival_products}
        return render(request,"index2.html",params)

class CartListView(ListView): 
    def get(self, request, *args, **kwargs):
        product = Product.objects.filter(is_active=True)
        # customer = Customers.objects.get(admin=request.user.id)
        param = {"product":product}
        return render(request,"cart.html",param)
 
class ProductFilterListView(ListView):

    def get(self, request, *args, **kwargs):
        caties = ProductCategory.objects.filter(is_active=True)
        subCaties = ProductSubCategory.objects.filter(is_active=True)
        childSubCaties = ProductChildSubCategory.objects.filter(is_active=True)
        products = Product.objects.filter(is_active=True)        

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
        params={'categories':categories_list,"cats":caties,"subcaties":subCaties,"product_list":products}
        return render(request,"product_filter_list.html",params)


    # def get(self,request,*args,**kwargs):
    #     caties = ProductCategory.objects.filter(is_active=True)
    #     subcaties = ProductSubCategory.objects.filter(is_active=True)
    #     products=Product.objects.filter(is_active=True)

        
    #     allprods=[]
    #     catprods=Product.objects.values('product_category')
    #     subcatprod=Product.objects.values('product_subcategory')
    #     # print(subcatprods)
    #     # print(catprods)
    #     subcatprods = {item['product_subcategory'] for item in subcatprod}
    #     cats={item['product_category'] for item in catprods}
    #     prod =[]
    #     for cat in cats:
    #         prods = Product.objects.filter(product_category=cat,is_active=1)
    #         # print(prods)
    #         prod =[]
    #         for product in prods: 
    #             media=productMedia.objects.filter(product=product).first()
    #             prod.append({"product":product,"media":media})            
    #         n=len(prod)
    #         # print(prod)
    #         nSlides=n//4 + ceil((n/4)-(n//4))
    #         productcategories = ProductCategory.objects.get(id=cat,is_active=1)
    #         # productsubcategories=[]
    #         # for productcategory in productcategories:
    #         #     productsubcategy = ProductSubCategory.objects.filter(category=productcategory,is_active=1)
    #         #     productsubcategories.append({productsubcategy})
            
    #         prodsub=ProductSubCategory.objects.filter(category=cat,is_active=1)
    #         allprods.append([prod,range(nSlides),nSlides,productcategories,prodsub])           
    #     # print(allprods)
    #     print(products)
    #     params={'allprods':allprods,"cats":caties,"subcaties":subcaties}
    #     return render(request,"product_filter_list.html",{'products_list':products})

def home_two(request):
    return render(request,'home_two.html')


def search_list(query=None):
    queryset = []
    queries = query.split(" ")
    for q in queries:
        Products = Product.objects.filter(
            (Q(Product_name__icontains = q) | Q(Product_desc__icontains = q)) & Q(is_verified=True) 
            ).distinct()

        for Product in Products:
            queryset.append(Product)
    
    return list(set(queryset)) 
 

class baseView(ListView):
    def get(self, request, *args, **kwargs):
        related_products = Product.objects.filter(is_active=1)
        catProduct=Product.objects.values('Product_category','id')
        cats={item['Product_category'] for item in catProduct}
        allcats=[]
        for cat in cats:
            allcat=ProductCategory.objects.get(id=cat)
            # crs=Product.objects.filter(Product_category=cat,is_verified=True)
            crscnt=Product.objects.filter(Product_category=cat).count()
            # nSlides=n/4+ceil((n/4)-(n//4))
            # Products.append(crs)
            allcats.append([allcat,crscnt])
        context = {'related_products':related_products}
        return render(request, 'product_detail.html', context)

class ProductDetailView(DetailView): 
    def get(self, request, *args, **kwargs):
        product = get_object_or_404(Product, product_slug=kwargs['product_slug'])
        related_products = Product.objects.filter(product_category=product.product_category,is_active=1)         
        media = productMedia.objects.filter(product=product)
        abouts = ProductDetails.objects.filter(product=product)
        product_stock=ProductStockManage.objects.get(product=product)
        context = {'product': product,'media':media,'abouts':abouts,'related_products':related_products,'product_stock':product_stock}
        print(related_products)
        return render(request, 'product_detail.html', context)

def basket_add(request):
    basket = Basket(request)
    if request.POST.get('action') == 'post':
        product_id_list=request.POST.getlist('productid[]')
        product_qty_list=request.POST.getlist('productqty[]')
       
        product_id = 0
        product_qty = 0
        print(product_id_list,product_qty_list)
        i=0
        for product in product_id_list:
            product_id = int(product)
            product_qty=product_qty_list[i]
            i=i+1 
            product = get_object_or_404(Product,id=product_id)
            # torder = TempOrder.objects.filter(amount=amount,product=product,quantity=product_qty_list[i],address=address,customer=request.user)
    #uses for basket good for excercise
            basket.add(product=product,qty=product_qty)
       
        # #return for popover total item in cart    
        response = JsonResponse({'data':product_qty_list})
        return response

def basket_delete(request):
    basket = Basket(request)
    if request.POST.get('action') == 'post':
        product_id=request.POST.get('productid')
        basket.delete(product=product_id)
        #return for popover total item in cart    
        response = JsonResponse({'Success':True})
        return response

def Product_list(request):
    stf=Staffs.objects.all()
    allcrs=Product.objects.all()
    Products=[]
    allcats=[]
    catProduct=Product.objects.values('Product_category','id')
    cats={item['Product_category'] for item in catProduct}
    for cat in cats:
        allcat=ProductCategory.objects.get(id=cat)
        # crs=Product.objects.filter(Product_category=cat,is_verified=True)
        crscnt=Product.objects.filter(Product_category=cat).count()
        # nSlides=n/4+ceil((n/4)-(n//4))
        # Products.append(crs)
        allcats.append([allcat,crscnt])

    Products=Product.objects.filter(is_verified=True)
    cnt=Product.objects.filter().count()
    # allcat=ProductCategory.objects.all()
    allsubcat=ProductSubCategory.objects.all()
    paginator=Paginator(Products,6)
    page=request.GET.get('page')
    Products=paginator.get_page(page)
    param={'allcat':allcats,'allsubcat':allsubcat,'Products1':Products,'cnt':cnt,'stf':stf,'allcrs':allcrs}
    return render(request,'Product_list.html',param)

def testing_file(request):
    allProduct=[]
    catProduct=Product.objects.values('Product_category','Product_code')
    cats={item['Product_category'] for item in catProduct}
    for cat in cats:
        crs=Product.objects.filter(Product_category=cat)
        n=len(crs)
        nSlides=n/4+ceil((n/4)-(n//4))    
        allProduct.append([crs,range(1,n),nSlides])
    # Products=Product.objects.all()
    # print(Products)
    # n=len(Products)
    # nSlides=n/3+ceil((n/4)-(n//4))
    #  params= {'no_of_slides':n, 'range':range(0,n), 'Product':Products}
    # print(params)
    params= {'allProduct':allProduct}
    print(crs)
    
    return render(request,'testing_file.html',params)
 
def Product_details_2(request):
    return render(request,'Product_details_2.html')

def dologout(request):
    logout(request)
    return redirect('/')

def about_us(request):
    stf=Staffs.objects.all()
    allcrs=Product.objects.all()
    param={'stf':stf,'allcrs':allcrs}
    return render(request,'about-us.html',param)

def career(request):
    return render(request,'career.html')

def contact_us(request):
    return render(request,'contact-us.html')

def AddUpdateCart(request):
    data = json.loads(request.body)
    print(data)
    item = data['item']
    quantity = data['quantity']   
   
    customer = request.user.customers
    product = Product.objects.get(id=item)
    cart, created = Cart.objects.get_or_create(customer=customer,complete=False,item=product)
    cart.quantity=quantity
    cart.save()

    if cart.quantity <= 0:
        cart.delete()
        
    # if action == 'add':
    #     cart.quantity == quantity
    # if action == 'remove':
    #      cart.quantity == quantity
    return JsonResponse('Item is added',safe=False)

class CheckoutListView(View):

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        # try:
        product = Product.objects.filter(is_active=True)
        customer = Customers.objects.get(admin=request.user.id)
        address = CustomersAddress.objects.filter(customer=customer)
        is_active_address = CustomersAddress.objects.get(customer=customer,is_active=True)
        is_default_address = CustomersAddress.objects.get(customer=customer,is_default=True)
        cart_helper = CartHelper(request.user.customers)
        checkout_details = cart_helper.prepare_cart_for_checkout()
        cart_list = []
        total_price = 0
        total_delivery_cost = 0
        total_discount = 0
        total_amount = 0
        amount = 0
        param = {}
        if checkout_details:
            products = checkout_details['products']            
            for product in products:
                cart_id=product['cart']
                cart = Cart.objects.get(id=cart_id)
                cart_list.append(cart)    
            
            totals = checkout_details['total']
            
            for total in totals:
                total_price = total['total_price']    
                total_discount = total['total_discount'] 

            amounts = checkout_details['amount']
           
            for amount in amounts:
                total_amount = amount['total_amount']     
                total_delivery = amount['delivery_cost']
                print("delivery cost")
                print(total_delivery)
                total_delivery_cost = total_delivery + total_delivery_cost
            total_delivery_cost = Decimal(total_delivery_cost)
            print(total_delivery_cost)
            amount = Decimal(total_amount)
            if total_delivery_cost != "False":
                amount = amount + Decimal(total_delivery_cost) 
           
        param = {"product":product,"customer":customer,"address":address,"is_active_address":is_active_address,"is_default_address":is_default_address,'cart_list':cart_list,'total_price':total_price,'total_discount':total_discount,'total_amount':amount,'total_delivery_cost':total_delivery_cost}              
        # except Exception as e:
            # param = {"product":product,"customer":customer,"address":address}      
        return render(request,"checkout.html",param)

    def post(self,request,*args, **kwargs):
        basket = Basket(request)
        paymet_method = request.POST.get("payment")
        cart_helper = CartHelper(request.user.customers)
        checkout_details = cart_helper.prepare_cart_for_checkout()
        products = checkout_details['products']
        cart_list = []
        total_price = 0
        total_delivery_cost = 0
        total_discount = 0
        total_amount = 0
        if checkout_details:
            products = checkout_details['products']            
            for product in products:
                cart_id=product['cart']
                cart = Cart.objects.get(id=cart_id)
                cart_list.append(cart)    
            
            totals = checkout_details['total']
            
            for total in totals:
                total_price = total['total_price']    
                total_discount = total['total_discount'] 

            amounts = checkout_details['amount']
           
            for amount in amounts:
                total_amount = amount['total_amount']     
                total_delivery = amount['delivery_cost']
                print("delivery cost")
                print(total_delivery)
                total_delivery_cost = total_delivery + total_delivery_cost
            total_delivery_cost = Decimal(total_delivery_cost)
            print(total_delivery_cost)
            amount = Decimal(total_amount)
            if total_delivery_cost != "False":
                amount = amount + Decimal(total_delivery_cost)
        
        # print(amount)
        product_Json = request.POST.get("product_Json")
        # try:
        customer = Customers.objects.get(admin=request.user.id)
        is_active_address = CustomersAddress.objects.get(customer=customer,is_active=True)
        order = Orders(payment_method=paymet_method,customer=customer,product_Json=product_Json,amount=amount,status = "Payment Process")
        order.address = is_active_address
        order.transaction_id = datetime.now().timestamp()
        order.save()
        print("order save")

        tracker = OrderTacker(ordes_id=order.id,desc="product purchase successfuly !")
        tracker.save()

        # thank =True
        # if thank:
        #     param = {'thank':thank}
        #     return render(request,"checkout.html",param)
        # else:
        param= {}
        currency = 'INR'
        amount = 20000   # Rs. 200

        # Create a Razorpay Order
        razorpay_order = razorpay_client.order.create(dict(amount=amount,
                                                        currency=currency,
                                                        payment_capture='0'))

        # order id of newly created order.
        razorpay_order_id = razorpay_order['id']
        callback_url = 'paymenthandler/'

        # we need to pass these details to frontend.
        
        param['razorpay_order_id'] = razorpay_order_id
        param['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
        param['razorpay_amount'] = amount
        param['currency'] = currency
        param['callback_url'] = callback_url

        response = JsonResponse(param)
        return response
        # return HTTPResponse(param)
        # except:
        #     messages.add_message(request,messages.ERROR,"Connection Error Try Again")
        #     # return HttpResponse("error in connection")
        #     return HttpResponseRedirect(reverse("checkout"))


def RazorpayPayment(request):

	currency = 'INR'
	amount = 20000   # Rs. 200

	# Create a Razorpay Order
	razorpay_order = razorpay_client.order.create(dict(amount=amount,
													currency=currency,
													payment_capture='0'))

	# order id of newly created order.
	razorpay_order_id = razorpay_order['id']
	callback_url = 'paymenthandler/'

	# we need to pass these details to frontend.
	context = {}
	context['razorpay_order_id'] = razorpay_order_id
	context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
	context['razorpay_amount'] = amount
	context['currency'] = currency
	context['callback_url'] = callback_url

	return render(request, 'razorpay.html', context=context)


# we need to csrf_exempt this url as
# POST request will be made by Razorpay
# and it won't have the csrf token.
@csrf_exempt
def paymenthandler(request):

	# only accept POST request.
	if request.method == "POST":
		try:		
			# get the required parameters from post request.
			payment_id = request.POST.get('razorpay_payment_id', '')
			razorpay_order_id = request.POST.get('razorpay_order_id', '')
			signature = request.POST.get('razorpay_signature', '')
			params_dict = {
				'razorpay_order_id': razorpay_order_id,
				'razorpay_payment_id': payment_id,
				'razorpay_signature': signature
			}

			# verify the payment signature.
			result = razorpay_client.utility.verify_payment_signature(
				params_dict)
			if result is None:
				amount = 20000 # Rs. 200
				try:

					# capture the payemt
					razorpay_client.payment.capture(payment_id, amount)

					# render success page on successful caputre of payment
					return render(request, 'paymentsuccess.html')
				except:

					# if there is an error while capturing payment.
					return render(request, 'paymentfail.html')
			else:

				# if signature verification fails.
				return render(request, 'paymentfail.html')
		except:

			# if we don't find the required parameters in POST data
			return HttpResponseBadRequest()
	else:
	# if other than POST request is made.
		return HttpResponseBadRequest()

