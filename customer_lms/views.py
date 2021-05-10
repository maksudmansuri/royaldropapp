# from django.shortcuts import render,redirect,HttpResponseRedirect
# from .forms import RegisterForm
# from django.contrib.auth import login,authenticate,logout
# #from django.contrib.auth.models import User
# from front.models import Product,Product_Session,Product_Modules,ProductCategory,ProductSubCategory
# # from .models import Orders,Ratting,paytm_payment
# from accounts.models import Customers as Customers,CustomUser
# from front.models import viewed,ProductComments
# from django.contrib import messages
# from django.contrib.auth.forms import UserChangeForm
# from django.core.files.storage import FileSystemStorage
# from django.contrib.auth.decorators import login_required
# from django.core.paginator import Page,PageNotAnInteger,Paginator
# import moviepy.editor
# from front.views import search_list
# from django.views.decorators.csrf import csrf_exempt
# from .paytm import Checksum
# # Create your views  h ere.
# MERCHANT_KEY = 'bBzG2&6OfWiZzlT0'

# def customer_logout(request):
#     logout(request)
#     return redirect('/accounts/dologin')

# @login_required
# def lms_base(request):
#     std=Customers.objects.get(admin=request.user.id)
#     return render(request,'customer_lms/lms_base.html',{'std1':std})
    
# @login_required
# def customer_dashboard(request):
#     std=Customers.objects.get(admin=request.user)
#     # ordcrs=Orders.objects.filter(customer=std)
#     cntssns=0
#     per=0
#     tlssns=0
#     vwdsns=0
#     allinone = []
#     for ord in ordcrs:
#         getvwd=viewed.objects.get(product=ord.product.id)
#         getcsr=Product.objects.get(id=ord.product.id)
#         getml=Product_Modules.objects.get(product=getcsr,position=int(getvwd.module_position))
#         getssn=Product_Session.objects.get(module=getml,position=int(getvwd.session_position))
#         cntmls=Product_Modules.objects.filter(product=ord.product)
#         for cntml in cntmls:
#             if cntml.position < int(getvwd.module_position):
#                 cntssns = Product_Session.objects.filter(module=cntml).count()
#                 tlssns=tlssns + cntssns
#                 vwdsns=vwdsns + cntssns
#                 print(tlssns)
#             elif cntml.position == int(getvwd.module_position):
#                 vwdssns = Product_Session.objects.filter(module=cntml)
#                 cntvwdssn=0
#                 for vwdssn in vwdssns:
#                     if vwdssn.position <= int(getvwd.session_position):
#                         vwdsns = vwdsns + 1
#                         tlssns=tlssns + 1
#                     else:
#                         tlssns=tlssns + 1
#             else:
#                 cntssns = Product_Session.objects.filter(module=cntml).count()
#                 tlssns=tlssns + cntssns
#         per = (vwdsns * 100) / tlssns
#         allinone.append([ord,getcsr,getml,getssn,per,vwdsns,tlssns])
#         print(allinone)   
#     param={'allinone':allinone,'std1':std}
#     return render(request,'customer_lms/customer_dashboard.html',param)

# @login_required
# def customer_account_edit_save(request):
#     if request.method == "POST":
#         std_id=request.POST['std_id']
#         fisrt_name=request.POST['fisrt_name']
#         last_name=request.POST['last_name']
#         address=request.POST['customer_address']
#         city=request.POST['customer_city']
#         state=request.POST['customer_state']
#         country=request.POST['customer_country']
#         qualification=request.POST['customer_qualification']
#         dob=request.POST['customer_dob']
#         phone=request.POST['customer_phone']
#         gender=request.POST['gender']

#         if request.FILES.get('photo'):
#             photo=request.FILES['photo']
#             fs=FileSystemStorage()
#             filename=fs.save(photo.name,photo)
#             photo_url=fs.url(filename)
#         else:
#             photo_url=None
#         try:
#             user=CustomUser.objects.get(id=std_id)
#             user.first_name=fisrt_name
#             user.last_name=last_name
#             user.save() 
                
#             std_model=Customers.objects.get(admin=std_id)
#             print(std_model)
#             std_model.fisrt_name=fisrt_name
#             std_model.last_name=last_name
#             std_model.address=address
#             std_model.city=city
#             std_model.state=state
#             std_model.country=country
#             std_model.qualification=qualification
#             std_model.dob=dob
#             std_model.phone=phone
#             if photo_url!=None:
#                 std_model.photo=photo_url
#                 print(std_model)
#             std_model.gender=gender
#             std_model.is_appiled=True
#             std_model.is_verified=False
#             std_model.save()

#             messages.success(request,"successfully Edited:")
#             return HttpResponseRedirect("/customer_lms/customer_account_edit")
#         except:
#             messages.success(request,"Failed To Edit:")
#             return HttpResponseRedirect("/customer_lms/customer_account_edit")
    
# @login_required
# def customer_account_edit(request):
#     std=Customers.objects.get(admin=request.user)
#     print(std.dob)
#     return render(request,'customer_lms/customer_account_edit.html',{'std1':std})
            
# def customer_account_edit_basic(request):
#     if request.user.is_anonymous:
#        return redirect("/accounts/dologin")
#     return render(request,'customer_lms/customer_account_edit_basic.html')

# def customer_account_edit_profile(request):
#     if request.user.is_anonymous:
#        return redirect("/accounts/dologin")
#     std=Customers.objects.get(admin=request.user.id)
#     return render(request,'customer_lms/customer_account_edit_profile.html',{'std1':std})

# def customer_billing(request):
#     if request.user.is_anonymous:
#        return redirect("/accounts/dologin")
#     return render(request,'customer_lms/customer_billing.html')

# @login_required
# def customer_browse_products(request):
#     std=Customers.objects.get(admin=request.user.id)
#     # query = ""
#     # if request.GET:
#     #     query = request.GET['q']
#     #     query=str(query)
    
#     crs=Product.objects.filter(is_verified=True)
#     paginator=Paginator(crs,6)
#     page=request.GET.get('page')
#     crs=paginator.get_page(page)
#     return render(request,'customer_lms/customer_browse_products.html',{'crs':crs,'std1':std})

# @login_required()
# def customer_cart(request,slug):
#     std=Customers.objects.get(admin=request.user.id)
#     crs=Product.objects.get(product_slug=slug)
#     if Orders.objects.filter(product=crs.id).exists():
#         messages.add_message(request,messages.ERROR,"Product already purchased")
#         return render(request,'customer_lms/customer_cart.html',{'crs1':crs,'std1':std})
#     if request.method=="POST":
#         user=Customers.objects.get(admin=request.user.id)
#         print(std.admin)
#         order=Orders(customer=user,product=crs,customer_phone=user.phone,customer_email=user.admin.email)
#         order.save()
#         return redirect(f"/customer_lms/customer_pay/{crs.product_slug}",kwargs={'crs1': crs,'std1':std}) 
#     return render(request,'customer_lms/customer_cart.html',{'crs1':crs,'std1':std})

# @login_required() 
# def customer_help_center(request):
#     if request.user.is_anonymous:
#        return redirect("/accounts/dologin")
#     return render(request,'customer_lms/customer_help_center.html')

# @login_required()
# def customer_fail(request):    
#     return render(request,'customer_lms/customer_fail.html')

# @login_required()
# def customer_invoice(request,id):
#     cnf_ord=paytm_payment.objects.get(ORDERID=id)
#     ord=Orders.objects.get(id=id)
#     std=Customers.objects.get(admin=request.user.id)
#     return render(request,'customer_lms/customer_invoice.html',{'cnf_ord':cnf_ord,'std1':std,'ord':ord})

# def customer_messages(request):
#     std=Customers.objects.get(admin=request.user)

#     return render(request,'customer_lms/customer_messages.html')

# def customer_messages_2(request):
#     if request.user.is_anonymous:
#        return redirect("/accounts/dologin")
#     return render(request,'customer_lms/customer_messages_2.html')

# @login_required()
# def customer_my_products(request):
#     std=Customers.objects.get(admin=request.user)
#     ordcrs=Orders.objects.filter(customer=std)
#     cntssns=0
#     per=0
#     tlssns=0
#     vwdsns=0
#     allinone = []
#     for ord in ordcrs:
#         getvwd=viewed.objects.get(customer=std,product=ord.product.id)
#         getcsr=Product.objects.get(id=ord.product.id)
#         print(getcsr)
#         getml=Product_Modules.objects.get(product=getcsr,position=int(getvwd.module_position))
#         print(getml)
#         getssn=Product_Session.objects.get(module=getml,position=int(getvwd.session_position))
#         print(getssn)
#         cntmls=Product_Modules.objects.filter(product=ord.product)
#         for cntml in cntmls:
#             if cntml.position < int(getvwd.module_position):
#                 cntssns = Product_Session.objects.filter(module=cntml).count()
#                 tlssns=tlssns + cntssns
#                 vwdsns=vwdsns + cntssns
#             elif cntml.position == int(getvwd.module_position):
#                 vwdssns = Product_Session.objects.filter(module=cntml)
#                 cntvwdssn=0
#                 for vwdssn in vwdssns:
#                     if vwdssn.position <= int(getvwd.session_position):
#                         vwdsns = vwdsns + 1
#                         tlssns=tlssns + 1
#                     else:
#                         tlssns=tlssns + 1
#             else:
#                 cntssns = Product_Session.objects.filter(module=cntml).count()
#                 tlssns=tlssns + cntssns
#         per = (vwdsns * 100) / tlssns
#         allinone.append([ord,getcsr,getml,getssn,per,vwdsns,tlssns])   
#     paginator=Paginator(allinone,6)
#     page=request.GET.get('page')
#     allinone=paginator.get_page(page)
#     param={'allinone':allinone,'std1':std}      
#     return render(request,'customer_lms/customer_my_products.html',param)

# def customer_pay(request,slug):
#     std=Customers.objects.get(admin=request.user.id)
#     crs=Product.objects.get(product_slug=slug)
#     ords=Orders.objects.get(product=crs.id)
#     param_dict = {
#             'MID':'VCqddy35812500980656',
#             'ORDER_ID':str(ords.id),
#             'TXN_AMOUNT':str(5000),
#             'CUST_ID':request.user.email,
#             'INDUSTRY_TYPE_ID':'Retail',
#             'WEBSITE':'WEBSTAGING',
#             'CHANNEL_ID':'WEB',
# 	        'CALLBACK_URL':'http://127.0.0.1:8000/customer_lms/handlerequest',
#     }
#     param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)
#     return render(request,'customer_lms/paytm.html',{'param_dict':param_dict,'std1':std})

#     # return render(request,'customer_lms/customer_pay.html',{'std1':std})

# @csrf_exempt
# def handlerequest(request):
#     form=request.POST
#     response_dict = {}
#     for i in form.keys():
#         response_dict[i] = form[i]
#         if i == 'CHECKSUMHASH':
#             checksum = form[i]
#     verify = Checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
#     print(response_dict)    
#     CURRENCY = request.POST['CURRENCY']
#     GATEWAYNAME = request.POST['GATEWAYNAME']
#     RESPMSG = request.POST['RESPMSG']
#     BANKNAME = request.POST['BANKNAME']
#     PAYMENTMODE = request.POST['PAYMENTMODE']
#     RESPCODE = request.POST['RESPCODE']
#     TXNID = request.POST['TXNID']
#     TXNAMOUNT = request.POST['TXNAMOUNT']
#     ORDERID = request.POST['ORDERID']
#     STATUS = request.POST['STATUS']
#     BANKTXNID = request.POST['BANKTXNID']
#     TXNDATE = request.POST['TXNDATE']
#     ord_cmf=paytm_payment(CURRENCY=CURRENCY,
#     GATEWAYNAME=GATEWAYNAME,
#     RESPMSG=RESPMSG,
#     BANKNAME=BANKNAME,
#     PAYMENTMODE=PAYMENTMODE,
#     RESPCODE=RESPCODE,
#     TXNID=TXNID,
#     TXNAMOUNT=TXNAMOUNT,
#     ORDERID=ORDERID,
#     STATUS=STATUS,
#     BANKTXNID=BANKTXNID,
#     TXNDATE=TXNDATE)
#     ord_cmf.save()
#     if verify:
#         if response_dict['RESPCODE'] == '01':
#             print('order Successful')
#         else:
#             print('order was not successful because' + response_dict['RESPMSG'])
#     return render(request,'customer_lms/paytm_status.html',{'response':response_dict})
             
# def customer_quiz_results(request):
#     if request.session.has_key('logged in'):
#         if request.user.user_type!="3":
#             messages.error(request,"Invvalid Page :")
#             return redirect("/accounts/dologin")
#         return render(request,'customer_lms/customer_quiz_results.html')
#     return redirect("/accounts/dologin")

# def convert(seconds):
#     hours = seconds // 3600
#     seconds %= 3600
#     mins = seconds // 60
#     seconds %= 60
#     return hours, mins, seconds

# @login_required()
# def session(request,product_slug,slug):
#     std=Customers.objects.get(admin=request.user.id)
#     crs=Product.objects.get(product_slug=product_slug,)
#     allml=Product_Modules.objects.filter(product=crs)
#     ml=Product_Modules.objects.get(slug=slug,product=crs)
#     allssn=Product_Session.objects.filter(module=ml)
#     lastssn=Product_Session.objects.filter(module=ml).last()
#     getvwssn=lastssn.position + 1
#     crssn2=Product_Session.objects.filter(module=ml)
#     param={'crs':crs,'allssn':allssn,'ssn':crssn2,'std1':std,'ml':ml,'getvwssn':getvwssn}
#     return render(request,'customer_lms/session.html',param)
#     # return redirect("/accounts/dologin")

# @login_required()
# def session_seen(request,product_slug,slug,sslug):
#     std=Customers.objects.get(admin=request.user.id)
#     crs=Product.objects.get(product_slug=product_slug)
#     allml=Product_Modules.objects.filter(product=crs)
#     ml=Product_Modules.objects.get(slug=slug,product=crs)
#     allssn=Product_Session.objects.filter(module=ml)
#     crssn2=Product_Session.objects.get(product_slug=sslug,module=ml)
#     cmmnts=ProductComments.objects.filter(session=crssn2)
#     param={'crs':crs,'allssn':allssn,'ssn':crssn2,'std1':std,'ml':ml,'cmmnts':cmmnts}
#     return render(request,'customer_lms/session_seen.html',param)

# @login_required()
# def session_view(request,product_slug,slug,sslug):
#     std=Customers.objects.get(admin=request.user)
#     crs=Product.objects.get(product_slug=product_slug)
#     allml=Product_Modules.objects.filter(product=crs)
#     ml=Product_Modules.objects.get(slug=slug,product=crs)
#     allssn=Product_Session.objects.filter(module=ml)
#     lastssn=Product_Session.objects.filter(module=ml).last()
#     lastml=Product_Modules.objects.filter(product=crs).last()
#     crssn2=Product_Session.objects.get(product_slug=sslug,module=ml)
#     cmmnts=ProductComments.objects.filter(session=crssn2)
#     print(crs)
#     print(std)
#     print(ml)
#     print(lastssn)
#     print(lastml)
#     print(crssn2)
#     vwd1=viewed.objects.get(customer=std,product=crs.id)
#     print(vwd1)
#     getvwssn=int(vwd1.session_position)
#     getvwml=int(vwd1.module_position)
#     if request.method == "POST":
#         product=request.POST['ccrs']
#         module=request.POST['cmdl']
#         session=int(request.POST['cssn'])
#         if viewed.objects.filter(customer=std,product=product).exists():
#             vwd=viewed.objects.get(customer=std,product=product)
#             this=int(vwd.session_position)
#             that=int(vwd.module_position)  
#             if this == getvwssn:
#                 if this == lastssn.position:
#                     if that == lastml.position:
#                         pass
#                     else:
#                         that = that + 1 
#                         this=1
#                 else:
#                     this=session+1
#             elif this < getvwssn:
#                 this = session
#             else:
#                 pass
#             vwd.session_position=this
#             vwd.module_position=that
#             vwd.save()
            
#     # getvwd=viewed.objects.filter(customer=std)
#     if viewed.objects.filter(customer=std,product=crs.id,module_position=ml.position).exists():
#         vwd=viewed.objects.get(customer=std,product=crs.id,module_position=ml.position)
#         getcsr=Product.objects.get(id=crs.id)
#         getml=Product_Modules.objects.get(position=int(ml.position),product=getcsr)
#         getssn=Product_Session.objects.get(position=int(vwd.session_position),module=getml)
#         getvwssn = int(vwd.session_position)

                  
#     param={'crs':crs,'allssn':allssn,'ssn':crssn2,'std1':std,'ml':ml,'getvwssn':getvwssn,'cmmnts':cmmnts,'getvwml':getvwml}
#     return render(request,'customer_lms/session_view.html',param)

# def sessionComment_view(request,product_slug,slug,sslug):
#     crs=Product.objects.get(product_slug=product_slug)
#     crs=Product.objects.get(product_slug=product_slug)
#     ml=Product_Modules.objects.get(slug=slug,product=crs)
#     ssn=Product_Session.objects.get(module=ml,product_slug=sslug)
#     if request.method=="POST":
#         user = request.user
#         session = ssn
#         comment = request.POST.get("comment")

#         cmmnt=ProductComments(user=user,session=session,comment=comment)
#         cmmnt.save()
#         messages.add_message(request,messages.SUCCESS,"Comment Posted Successfuly")

#     return redirect(f"/customer_lms/session_view/{crs.product_slug}/{ml.slug}/{ssn.product_slug}") 

# def sessionComment(request,product_slug,slug,sslug):
#     crs=Product.objects.get(product_slug=product_slug)
#     crs=Product.objects.get(product_slug=product_slug)
#     ml=Product_Modules.objects.get(slug=slug,product=crs)
#     ssn=Product_Session.objects.get(module=ml,product_slug=sslug)
#     if request.method=="POST":
#         user = request.user
#         session = ssn
#         comment = request.POST.get("comment")

#         cmmnt=ProductComments(user=user,session=session,comment=comment)
#         cmmnt.save()
#         messages.add_message(request,messages.SUCCESS,"Comment Posted Successfuly")

#     return redirect(f"/customer_lms/session_seen/{crs.product_slug}/{ml.slug}/{ssn.product_slug}")

# @login_required() 
# def modules(request,slug):
#     crssn=[]
#     getvwml=1
#     std=Customers.objects.get(admin=request.user.id)
#     crs=Product.objects.get(product_slug=slug)
#     mdl=Product_Modules.objects.filter(product=crs)   
#     getcsr=crs
#     getml=1
#     getssn=1
#     getvwml=1
#     if viewed.objects.filter(customer=std.id,product=crs.id).exists():
#         getmls = viewed.objects.get(customer=std,product=crs.id)
#         getml=Product_Modules.objects.get(product=crs,position=int(getmls.module_position))
#         getssn=Product_Session.objects.get(module=int(getmls.module_position),position=int(getmls.session_position))
#         getvwml = int(getmls.module_position)
#     else:
#         vd=viewed(customer=std,product=crs.id,module_position='1',session_position='1')
#         vd.save()
#         getmls = viewed.objects.get(customer=std,product=crs.id)
#         getml=Product_Modules.objects.get(product=crs,position=int(getmls.module_position))
#         getssn=Product_Session.objects.get(module=int(getmls.module_position),position=int(getmls.session_position))
#         getvwml = int(getmls.module_position)
#     for ml in mdl:
#         mlcrssn=Product_Session.objects.filter(module=ml)
#         n=len(mlcrssn)
#         crssn.append([mlcrssn,ml,n])
#     param={'crs1':crs,'crssn1':crssn,'std1':std,'getvwml':getvwml,'getcsr':getcsr,'getml':getml,'getssn':getssn}
#     return render(request,'customer_lms/modules.html',param)

# @login_required()
# def customer_take_product_session(request,product_slug,slug,sslug):
#     std=Customers.objects.get(admin=request.user.id)
#     crs=Product.objects.get(product_slug=product_slug)
#     allml=Product_Modules.objects.filter(product=crs)
#     ml=Product_Modules.objects.get(slug=slug,product=crs)
#     crssn2=Product_Session.objects.get(product_slug=sslug,module=ml)
#     crssn=[]        
#     allml=Product_Modules.objects.filter(product=crs)
#     for ml in allml:
#         mlcrssn=Product_Session.objects.filter(module=ml)
#         n=len(mlcrssn)
#         crssn.append([mlcrssn,ml])

#     param={'crs1':crs,'crssn1':crssn,'crssn2':crssn2,'std1':std}
#     return render(request,'customer_lms/customer_take_product_session.html',param)
#     # return redirect("/accounts/dologin")

# @login_required()
# def customer_take_product_session_view(request,slug,sslug):
#     if request.session.has_key('logged in'):
#         if request.user.user_type!="3":
#             messages.error(request,"Invvalid Page :")
#             return redirect("/accounts/dologin")
#         std=Customers.objects.get(admin=request.user.id)
#         crs=Product.objects.filter(product_slug=product_slug)
#         crssn=Product_Session.objects.filter(product_id=crs[0])
#         crssn2=Product_Session.objects.get(product_slug=slug)
#         param={'crs1':crs[0],'crssn1':crssn,'crssn2':crssn2,'std1':std}
#         return render(request,'customer_lms/customer_take_product_session.html',param)
#     return redirect("/accounts/dologin")

# @login_required() 
# def customer_take_product(request,slug):
#     crssn=[]
#     std=Customers.objects.get(admin=request.user.id)
#     crs=Product.objects.get(product_slug=slug)
#     mdl=Product_Modules.objects.filter(product=crs)
#     for ml in mdl:
#         mlcrssn=Product_Session.objects.filter(module=ml)
#         n=len(mlcrssn)
#         crssn.append([mlcrssn,ml])
#         print(crssn)
#     param={'crs1':crs,'crssn1':crssn,'std1':std}
#     return render(request,'customer_lms/customer_take_product.html',param)

# def customer_take_quiz(request):
#     if request.user.is_anonymous:
#        return redirect("/accounts/dologin")
#     return render(request,'customer_lms/customer_take_quiz.html')

# def customer_view_product(request):
#     if request.user.is_anonymous:
#        return redirect("/accounts/dologin")
#     return render(request,'customer_lms/customer_view_product.html')

# def customer_account_billing_payment_information(request):
#     if request.user.is_anonymous:
#        return redirect("/accounts/dologin")
#     return render(request,'customer_lms/customer_account_billing_payment_information.html')

# def customer_account_billing_subscription(request):
#     if request.user.is_anonymous:
#        return redirect("/accounts/dologin")
#     return render(request,'customer_lms/customer_account_billing_subscription.html')

# def customer_account_billing_upgrade(request):
#     if request.user.is_anonymous:
#        return redirect("/accounts/dologin")
#     return render(request,'customer_lms/customer_account_billing_upgrade.html')

# def customer_forum(request):
#     if request.user.is_anonymous:
#        return redirect("/accounts/dologin")
#     return render(request,'customer_lms/customer_forum.html')

# def customer_forum_ask(request):
#     if request.user.is_anonymous:
#        return redirect("/accounts/dologin")
#     return render(request,'customer_lms/customer_forum_ask.html')

# def customer_forum_thread(request):
#     if request.user.is_anonymous:
#        return redirect("/accounts/dologin")
#     return render(request,'customer_lms/customer_forum_thread.html')

# def customer_profile(request):
#     if request.user.is_anonymous:
#        return redirect("/accounts/dologin")
#     return render(request,'customer_lms/customer_profile.html')

# def customer_profile_posts(request):
#     if request.user.is_anonymous:
#        return redirect("/accounts/dologin")
#     return render(request,'customer_lms/customer_profile_posts.html')

