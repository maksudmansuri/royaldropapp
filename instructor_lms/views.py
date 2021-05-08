from django.shortcuts import render,redirect, get_object_or_404,HttpResponseRedirect
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.models import User
from django.contrib import messages
from front.models import ProductSubCategory,ProductCategory,Product,Product_Session,Product_Modules
from accounts.models import Staffs,CustomUser
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
from django.template.defaultfilters import slugify
from .forms import CreateProduct,CreateSession
from django.core.paginator import Paginator,PageNotAnInteger,Page
from django.utils.safestring import mark_safe
from django.template import Library
from django.db.models import Q

import json


# Create your views here.
@login_required
def in_base(request):
    stf=Staffs.objects.get(admin=request.user.id)
    print(stf)
    return render(request,'instructor_lms/lms_base.html',{'stf1':stf})

@login_required
def instructor_dashboard(request):
    stf=Staffs.objects.get(admin=request.user)
    return render(request,'instructor_lms/instructor_dashboard.html',{'stf1':stf})

@login_required
def instructor_account_edit(request):
    stf=Staffs.objects.get(admin=request.user)
    print(stf)
    allcat=ProductSubCategory.objects.all()
    return render(request,'instructor_lms/instructor_account_edit.html',{'stf1':stf,'allcat':allcat})

@login_required  
def instructor_account_edit_save(request):
    stf=Staffs.objects.get(admin=request.user)
    if request.method == "POST":
        stf_id=request.POST['stf_id']
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        address=request.POST['address']
        dob=request.POST['dob']
        state=request.POST['state']
        city=request.POST['city']
        mobile=request.POST['mobile']
        country=request.POST['country']
        gender=request.POST['gender']
        qualification=request.POST['qualification']
        specialist=request.POST['specialist']
        experience=request.POST['experience']
        working_with=request.POST['working_with']
        website=request.POST['website']
        linkdin=request.POST['linkdin']
       
                
        if request.FILES.get('resume'):
            resume=request.FILES['resume']
            fs=FileSystemStorage()
            filename=fs.save(resume.name,resume)
            resume_url=fs.url(filename)
        else:
            resume_url=None

        if request.FILES.get('instructor_photo'):
            instructor_photo=request.FILES['instructor_photo']
            fs=FileSystemStorage()
            filename=fs.save(instructor_photo.name,instructor_photo)
            instructor_photo_url=fs.url(filename)
        else:
            instructor_photo_url=None
        try:

            user=CustomUser.objects.get(id=stf_id)
            user.first_name=first_name
            user.last_name=last_name
            user.save() 
                
            std_model=Staffs.objects.get(admin=stf_id)
            std_model.first_name=first_name
            std_model.last_name=last_name
            std_model.address=address
            std_model.city=city
            std_model.state=state
            std_model.country=country
            std_model.mobile=mobile
            std_model.dob=dob 
            if instructor_photo_url!=None:
                std_model.instructor_photo=instructor_photo_url
            std_model.gender=gender
            std_model.linkdin=linkdin
            std_model.website=website
            std_model.working_with=working_with
            std_model.experience=experience
            std_model.specialist=specialist
            std_model.qualification=qualification
           
            if resume_url!=None:
                std_model.resume=resume_url
            std_model.is_appiled=True
            std_model.is_verified=False
            std_model.save()
            
            messages.success(request,"successfully Addded details:")
            return redirect("/instructor_lms/instructor_account_edit")
        except:
            messages.error(request,"Failed To Edit:")
            return redirect("/instructor_lms/instructor_account_edit")

@login_required 
def instructor_products(request):
    stf=Staffs.objects.get(admin=request.user)
    crss=Product.objects.filter(teacher=stf)
    # pagenition for products in instructor 
    print(crss)
    paginator=Paginator(crss,6)
    page=request.GET.get('page')
    crss=paginator.get_page(page)
    return render(request,'instructor_lms/instructor_products.html',{'crss':crss,'stf1':stf})

@login_required
def instructor_product_publish(request,slug):
    stf=Staffs.objects.get(admin=request.user)
    crss=Product.objects.filter(teacher=stf)
    fcrs=get_object_or_404(Product,product_slug=slug)
    mdl=Product_Modules.objects.filter(product=fcrs)
    cnt=0
    
    if fcrs.is_appiled == False and fcrs.is_verified == False:
        for ml in mdl:
            crssn=Product_Session.objects.filter(module=ml)
            for ssn in crssn:
                cnt=cnt+1
    else:
        messages.add_message(request,messages.ERROR,"Product already verified")
    if stf.is_verified == True:
        if cnt > 0:
            fcrs.is_verified =False
            fcrs.is_appiled=True
            fcrs.save()
        else:
            messages.add_message(request,messages.ERROR,"Add atlest one Session first")
    elif stf.is_appiled == True:
        messages.add_message(request,messages.ERROR," Wait for account verification ")  
    else:
        messages.add_message(request,messages.ERROR," Complete you profile first")        
    paginator=Paginator(crss,6)
    page=request.GET.get('page')
    crss=paginator.get_page(page)
    return render(request,'/instructor_lms/instructor_products.html',{'crss':crss,'stf1':stf})

@login_required
def instructor_product_add(request):
    stf=Staffs.objects.get(admin=request.user)
    form=CreateProduct()
    allcat=ProductCategory.objects.all()
    allsubcat=ProductSubCategory.objects.all()
    allcrs=Product.objects.all()
    if request.method=="POST":
        crssubcat=get_object_or_404(ProductSubCategory,subcategory=request.POST['subcategory'])
        stf=Staffs.objects.get(admin=request.user)
        product_category=(crssubcat.category)
        product_name=request.POST['product_name']
        product_subcategory=crssubcat
        product_fee=request.POST['product_fee']
        teacher=stf
        product_duration=request.POST['product_duration']
        product_video=request.POST['product_video']
        product_level=request.POST['product_level']
        product_slug=slugify(request.POST['product_name'])
        if request.FILES.get('product_image'):
            product_image=request.FILES['product_image']
            fs=FileSystemStorage()
            filename=fs.save(product_image.name,product_image)
            product_image_url=fs.url(filename)
        else:
            product_image_url=None
        form=CreateProduct(request.POST)
        if form.is_valid():
            crs=form.save(commit=False)
            crs.product_category=product_category
            crs.product_name=product_name
            crs.product_subcategory=product_subcategory
            crs.product_fee=product_fee
            crs.teacher=teacher
            crs.product_duration=product_duration
            crs.product_video=product_video
            crs.product_level=product_level
            crs.product_slug=product_slug
            if product_image_url!=None:
                crs.product_image=product_image_url
            crs.save()
            return redirect("/instructor_lms/instructor_products")
        else:
            form=CreateProduct()
    return render(request,'instructor_lms/instructor_product_add.html',{'allsubcat1':allsubcat,'form':form,'stf1':stf})

@login_required
def instructor_product_add_save(request):
    if request.method=="POST":
        stf=Staffs.objects.get(admin=request.user)
        crssubcat=ProductSubCategory.objects.filter(subcategory=request.POST['product_subcategory'])
        print(crssubcat.category)
        product_category=request.POST['product_subcategory']
    return render(request,'instructor_lms/instructor_product_add.html',{'stf1':stf})

@login_required
def instructor_product_edit(request,slug):
    stf=Staffs.objects.get(admin=request.user)
    fcrs=get_object_or_404(Product,product_slug=slug)
    allcat=ProductCategory.objects.all()
    allsubcat=ProductSubCategory.objects.all()
    crs=Product.objects.get(product_slug=slug)
    allcrs=Product.objects.all()
    # form=CreateProduct()
    if request.method != "POST":
        form=CreateProduct(request.POST or None, instance=fcrs)
        # if form.is_valid():
        #     form.save()
    else:
        crssubcat=ProductSubCategory.objects.get(subcategory=request.POST['subcategory'])
        stf=Staffs.objects.get(admin=request.user)
        product_category=(crssubcat.category)
        product_name=request.POST['product_name']
        product_subcategory=crssubcat
        product_fee=request.POST['product_fee']
        teacher=stf
        product_duration=request.POST['product_duration']
        product_video=request.POST['product_video']
        product_level=request.POST['product_level']
        product_slug=slugify(request.POST['product_name'])
        if request.FILES.get('product_image'):
            product_image=request.FILES['product_image']
            fs=FileSystemStorage()
            filename=fs.save(product_image.name,product_image)
            product_image_url=fs.url(filename)
        else:
            product_image_url=None
        form=CreateProduct(request.POST or None, instance=fcrs)
        if form.is_valid():
            crs1=form.save(commit=False)
            crs1.product_category=product_category
            crs1.product_name=product_name
            crs1.product_subcategory=product_subcategory
            crs1.product_fee=product_fee
            crs1.teacher=teacher
            crs1.product_duration=product_duration
            crs1.product_video=product_video
            crs1.product_level=product_level
            crs1.product_slug=product_slug
            if product_image_url!=None:
                crs1.product_image=product_image_url
            crs1.is_appiled=True
            crs1.is_verified=False
            crs1.save()
            return redirect("/instructor_lms/instructor_products")    
    return render(request,'instructor_lms/instructor_product_edit.html',{'crs':fcrs,'allsubcat':allsubcat,'allcat':allcat,'form':form,'stf1':stf})

@login_required
def instructor_earnings(request):
    if request.user.is_anonymous:
       return redirect("/accounts/dologin")
    return render(request,'instructor_lms/instructor_earnings.html')

@login_required
def instructor_edit_invoice(request):
    if request.user.is_anonymous:
       return redirect("/accounts/dologin")
    stf=Staffs.objects.get(admin=request.user)
    return render(request,'instructor_lms/instructor_edit_invoice.html',{'stf1':stf})

@login_required
def instructor_help_center(request):
    if request.user.is_anonymous:
       return redirect("/accounts/dologin")
    return render(request,'instructor_lms/instructor_help_center.html')

@login_required
def instructor_invoice(request):
    if request.user.is_anonymous:
       return redirect("/accounts/dologin")
    stf=Staffs.objects.get(admin=request.user)
    return render(request,'instructor_lms/instructor_invoice.html',{'stf1':stf})

@login_required
def instructor_module_add(request,slug):
    bool=True
    fcrs=get_object_or_404(Product,product_slug=slug)
    mdl=Product_Modules.objects.filter(product=fcrs)
    stf=Staffs.objects.get(admin=request.user)
    if request.method == "POST":
        product=fcrs
        module=None
        if mdl == None:
            bool=True
        else:
            for i in mdl:
                if i.module != request.POST['module'] and i.position != int(request.POST['position']):
                    bool=True
                else:
                    bool=False
                    msg=messages.error(request,"already haiviing same name or same position number:")               
                    break
        if bool!=False:
            module=request.POST['module']
            module_desc=request.POST['module_desc']
            position=request.POST['position']
            slug=slugify(request.POST['module'])
            try:
                module=Product_Modules(product=product,module=module,position=position,module_desc=module_desc,slug=slug)
                module.save()
                fcrs.is_verified=False
                fcrs.is_appiled=False
                fcrs.save()
                mdl=Product_Modules.objects.filter(product=fcrs)
                messages.success(request,"successfully Addded details:")
            except:
                messages.error(request,"ISSUE WITH MODULE Addded details:")              
        else:
            messages.error(request,msg)
    return render(request,'instructor_lms/instructor_module_add.html',{'fcrs':fcrs,'crssn':mdl,'stf1':stf})
    # return redirect("/accounts/dologin")

@login_required
def instructor_module_edit(request,slug,sslug):
    bool=True
    stf=Staffs.objects.get(admin=request.user)
    fcrs=get_object_or_404(Product,product_slug=slug)
    allmdl=Product_Modules.objects.filter(product=fcrs)
    mdl=Product_Modules.objects.get(slug=sslug)
    return render(request,'instructor_lms/instructor_module_edit.html',{'fcrs':fcrs,'crssn':mdl,'allssn':allmdl,'stf1':stf})
 
@login_required
def instructor_module_edit_save(request,slug):
    # if request.session.has_key('logged in'):
    #     if request.user.user_type!="2":
    #         messages.error(request,"Invvalid Page :")
    #         return redirect("/accounts/dologin")
    #     else:
    stf=Staffs.objects.get(admin=request.user)
    fcrs=Product.objects.get(product_slug=slug)
    allmdl=Product_Modules.objects.filter(product=fcrs)
    crssn=Product_Modules.objects.get(id=request.POST['ssnid'])
    if request.method == "POST":
        product=crssn.product
        module=None
        if allmdl == None:
            bool=True
        else:
            for i in allmdl:
                if i.module != request.POST['module'] and i.position != int(request.POST['position']):
                    bool=True
                else:
                    if crssn.module == request.POST['module'] and crssn.position == int(request.POST['position']):
                        bool=True
                    else:
                        bool=False
                        msg=messages.error(request,"all ready have same name or position:")               
                        break
        if bool!=False:
            module=request.POST['module']
            module_desc=request.POST['module_desc']
            position=request.POST['position']
            slug=slugify(request.POST['module'])
            try:
                crssn.product=product
                crssn.module=module
                crssn.module_desc=module_desc
                crssn.slug=slug
                crssn.position=position
                crssn.save()
                fcrs.is_verified=False
                fcrs.is_appiled=False
                fcrs.save()                        
                messages.success(request,"successfully Addded details:")
            except:
                messages.error(request,"Error in Addding details:")               
        else:
            messages.error(request,msg)
    allmdl=Product_Modules.objects.filter(product=fcrs)
    return render(request,'instructor_lms/instructor_module_add.html',{'fcrs':fcrs,'crssn':allmdl,'stf1':stf})
   
from moviepy.video.io.VideoFileClip import VideoFileClip

@login_required
def instructor_lesson_add(request,slug,sslug):
    bool=True
    stf=Staffs.objects.get(admin=request.user)
    fcrs=get_object_or_404(Product,product_slug=slug)
    mdl=Product_Modules.objects.get(slug=sslug)
    crssn=Product_Session.objects.filter(module=mdl)
    if request.method=="POST":
        module=mdl
        # if Product_Session.objects.filter(session_name=request.POST['session_name'],module=mdl).exist():
        #     messages.add_message(request, messages.ERROR,"already haviing same session name:")
        #     return render(request,'instructor_lms/instructor_lesson_add.html',{'fcrs':fcrs,'crssn':crssn,'mdl':mdl})
        session_name=None
        if crssn == None:
            bool=True
        else:
            for i in crssn:
                if i.session_name != request.POST['session_name'] and i.position != int(request.POST['position']):
                    bool=True
                    print(i.position)
                    print(request.POST['position'])
                else:
                    bool=False
                    msg=messages.error(request,"already haviing same product name:")
                    break
        if bool!=False:
            session_name=request.POST['session_name']
            session_desc=request.POST['session_desc']
            session_duration=request.POST['session_duration']
            position=request.POST['position']
            product_slug=slugify(request.POST['session_name'])
            
            if request.FILES.get('product_in_pdf'):
                product_in_pdf=request.FILES['product_in_pdf']
                fs=FileSystemStorage()
                filename=fs.save(product_in_pdf.name,product_in_pdf)
                product_in_pdf_url=fs.url(filename)
            else:
                product_in_pdf_url=None

            if request.FILES.get('video_link'):
                video_link=request.FILES['video_link']
                fs=FileSystemStorage()
                filename=fs.save(video_link.name,video_link)
                video_link_url=fs.url(filename)
            else:
                video_link_url=None
            # clip = VideoFileClip("video_link_url")
            # print(clip.duration)
            a=1
            if a==1:
                session=Product_Session(module=module,session_desc=session_desc,session_duration=session_duration,position=position,product_slug=product_slug)
                if product_in_pdf_url != None:
                    session.product_in_pdf=product_in_pdf_url
                if video_link_url != None:
                    session.video_link=video_link_url
                session.session_name=session_name
                session.save()
                fcrs.is_verified=False
                fcrs.is_appiled=False
                fcrs.save()                        
                messages.success(request,"successfully Addded details:")
            # except:
            #     messages.error(request,"problemm with data in  Addded:")               
        else:
            messages.error(request,msg) 
    crssn=Product_Session.objects.filter(module=mdl)           
    return render(request,'instructor_lms/instructor_lesson_add.html',{'fcrs':fcrs,'crssn':crssn,'mdl':mdl,'stf1':stf})
    
@login_required
def instructor_lesson_edit(request,slug,sslug,ssslug):
    stf=Staffs.objects.get(admin=request.user)
    fcrs=Product.objects.get(product_slug=slug)
    mdl=Product_Modules.objects.get(slug=sslug,product=fcrs)
    allssn=Product_Session.objects.filter(module=mdl)
    crssn=Product_Session.objects.get(product_slug=ssslug,module=mdl)
            # crssn=get_object_or_404(Product_Session,product_slug=sslug,product_id=fcrs.id)
    return render(request,'instructor_lms/instructor_lesson_edit.html',{'fcrs':fcrs,'crssn':crssn,'allssn':allssn,'mdl':mdl,'stf1':stf})

@login_required
def instructor_lesson_edit_save(request,slug,sslug):
    stf=Staffs.objects.get(admin=request.user)
    fcrs=Product.objects.get(product_slug=slug)
    mdl=Product_Modules.objects.get(slug=sslug,product=fcrs)
    allssn=Product_Session.objects.filter(module=mdl)
    crssn=Product_Session.objects.get(id=request.POST['ssnid'])
    print(crssn)
    if request.method == "POST":
        module=crssn.module
        session_name=None
        if allssn == None:
            bool=True
        elif crssn == None:
            bool=False
            msg=messages.error(request,"selsected wrong name:")  
        else:
            for i in allssn:
                if i.session_name != request.POST['session_name']  and int(i.position != request.POST['position']):
                    bool=True
                else:
                    if crssn.session_name == request.POST['session_name'] and crssn.position != int(request.POST['position']):
                        bool=True
                    else:
                        bool=False
                        msg=messages.error(request,"all ready have same name:")               
                        break
        if bool!=False:
            session_name=request.POST['session_name']
            session_desc=request.POST['session_desc']
            position=request.POST['position']
            session_duration=request.POST['session_duration']
            video_link=request.POST['video_link']
            product_slug=slugify(request.POST['session_name'])

            if request.FILES.get('product_in_pdf'):
                product_in_pdf=request.FILES['product_in_pdf']
                fs=FileSystemStorage()
                filename=fs.save(product_in_pdf.name,product_in_pdf)
                product_in_pdf_url=fs.url(filename)
            else:
                product_in_pdf_url=None
                    # crssn1=Product_Session(crssn)
                    # print(crssn1)
            try:
                crssn.module=module
                crssn.session_name=session_name
                crssn.session_desc=session_desc
                crssn.session_duration=session_duration
                crssn.video_link=video_link
                crssn.product_slug=product_slug
                crssn.position=position
                    
                if product_in_pdf_url != None:
                    crssn.product_in_pdf=product_in_pdf_url
                crssn.save()
                fcrs.is_verified=False
                fcrs.is_appiled=False
                fcrs.save()
                        
                allssn=Product_Session.objects.filter(module=mdl)
                messages.success(request,"successfully Edited details:")
            except:
                messages.error(request,"Having a Problem with Database connection ")               
        else:
            messages.error(request,msg)
        return render(request,'instructor_lms/instructor_lesson_add.html',{'fcrs':fcrs,'crssn':allssn,'mdl':mdl,'stf1':stf}) 

@login_required
def instructor_messages(request):
    if request.user.is_anonymous:
       return redirect("/accounts/dologin")
    return render(request,'instructor_lms/instructor_messages.html')

@login_required
def instructor_quiz_edit(request):
    if request.user.is_anonymous:
       return redirect("/accounts/dologin")
    return render(request,'instructor_lms/instructor_quiz_edit.html')

@login_required
def instructor_quizzes(request):
    if request.user.is_anonymous:
       return redirect("/accounts/dologin")
    return render(request,'instructor_lms/instructor_quizzes.html')

@login_required
def instructor_review_quiz(request):
    if request.user.is_anonymous:
       return redirect("/accounts/dologin")
    return render(request,'instructor_lms/instructor_review_quiz.html')

@login_required
def instructor_statement(request):
    if request.user.is_anonymous:
       return redirect("/accounts/dologin")
    return render(request,'instructor_lms/instructor_statement.html')

@login_required
def instructor_forum(request):
    if request.user.is_anonymous:
       return redirect("/accounts/dologin")
    return render(request,'instructor_lms/instructor_forum.html')

@login_required
def instructor_forum_ask(request):
    if request.user.is_anonymous:
       return redirect("/accounts/dologin")
    return render(request,'instructor_lms/instructor_forum_ask.html')

@login_required
def instructor_forum_thread(request):
    if request.user.is_anonymous:
       return redirect("/accounts/dologin")
    return render(request,'instructor_lms/instructor_forum_thread.html')

@login_required
def instructor_profile(request):
    stf=Staffs.objects.get(admin=request.user)
    crs=Product.objects.filter(teacher=stf)
    param = {'crss':crs,'stf1':stf}
    return render(request,'instructor_lms/instructor_profile.html',param)

@login_required
def instructor_billing(request):
    if request.user.is_anonymous:
       return redirect("/accounts/dologin")
    return render(request,'instructor_lms/instructor_billing.html')

@login_required
def instructor_my_products(request):
    if request.user.is_anonymous:
       return redirect("/accounts/dologin")
    return render(request,'instructor_lms/instructor_my_products.html')

@login_required
def instructor_view_product(request,slug):
    stf=Staffs.objects.get(admin=request.user)
    param=[]
    crssn=[]
    # std=Students.objects.get(admin=request.user.id)
    crs=Product.objects.get(product_slug=slug)
    mdl=Product_Modules.objects.filter(product=crs)
    for ml in mdl:
        print(ml)
        mlcrssn=Product_Session.objects.filter(module=ml)
        print(mlcrssn)
        crssn.append([mlcrssn,ml])
    param={'crs1':crs,'crssn1':crssn,'stf1':stf}
    return render(request,'instructor_lms/instructor_view_product.html',param)

def check_product_session(request,slug,sslug,ssslug):
    # std=Students.objects.get(admin=request.user.id)
    stf=Staffs.objects.get(admin=request.user)
    crs=Product.objects.get(product_slug=slug)
    allml=Product_Modules.objects.filter(product=crs)
    ml=Product_Modules.objects.get(slug=sslug,product=crs)
    crssn2=Product_Session.objects.get(product_slug=ssslug,module=ml)
    crssn=[]        
    allml=Product_Modules.objects.filter(product=crs)
    
    for ml in allml:
        mlcrssn=Product_Session.objects.filter(module=ml)
        n=len(mlcrssn)
        crssn.append([mlcrssn,ml])
    
    param={'crs1':crs,'crssn1':crssn,'crssn2':crssn2,'stf1':stf}
    return render(request,'instructor_lms/check_product_session.html',param)

@login_required
def instructor_logout(request):
    logout(request)
    return redirect('/accounts/dologin')

@login_required
def delete_session(request,slug,sslug,ssslug):
    stf=Staffs.objects.get(admin=request.user)
    try:
        fcrs=Product.objects.get(product_slug=slug)
        mdl=Product_Modules.objects.get(slug=sslug,product=fcrs)
        allssn=Product_Session.objects.filter(module=mdl)
        crssn=Product_Session.objects.get(product_slug=ssslug,module=mdl).delete()
        messages.success(request," Delete successfully :")
    except:
        messages.error(request,"Not Deleted Try again if you want:")              
    return render(request,'instructor_lms/instructor_lesson_add.html',{'fcrs':fcrs,'crssn':allssn,'mdl':mdl,'stf1':stf})

@login_required
def delete_product(request,slug):
    stf=Staffs.objects.get(admin=request.user)
    fcrs=Product.objects.get(product_slug=slug).delete()
    return redirect("/instructor_lms/instructor_products")
    
@login_required
def delete_module(request,slug,sslug):
    stf=Staffs.objects.get(admin=request.user)
    fcrs=Product.objects.get(product_slug=slug)
    allmdl=Product_Modules.objects.filter(product=fcrs)
    mdl=Product_Modules.objects.get(slug=sslug,product=fcrs.id).delete()
    return render(request,'instructor_lms/instructor_module_add.html',{'fcrs':fcrs,'crssn':allmdl,'stf1':stf})
    

from django.http import JsonResponse

def test(request):
    if request.method == "POST":
        filesize = request.cookies.get('filesize')
        file=request.Files["file"]

        print(f"Filesize:{filesize}")
        print(file)
        return JsonResponse({"message":f"{file.filename} uploaded"})
    return render(request,"instructor_lms/test.html")

