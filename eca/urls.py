"""OC3 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from eca import settings
from django.conf.urls.static import static,__dict__
from django.contrib.auth import views as auth_views
from django.urls import path, reverse_lazy
from django.views.generic.base import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ecadmin/',include('ecaadmin.urls')),
    # path('admin', RedirectView.as_view(url=reverse_lazy('admin:index'))),
    # path('systemadmin/', admin.site.urls,name="admin_login"),
    #socialmedialogin url
    # path('oauth/', include('social_django.urls', namespace='social')), 
    # path('saccount/',include('allauth.urls'),name='saccount'),    
    path('ckeditor/', include('ckeditor_uploader.urls')),
    # path('chat/', include('chat.urls'),name='chat'),
    path('', include("front.urls")),
    # path('customer_lms/', include("customer_lms.urls")),
    # path('staff_lms/', include("staff_lms.urls")),
    # path('counsellor/', include("counsellor.urls")),
    path('accounts/', include("accounts.urls")),
    path('account/', include("django.contrib.auth.urls")),

    #Rest Framework Urls
    path('api/front/',include("front.api.urls")),
    path('api/accounts/',include("accounts.api.urls")),
    path('api/cart/',include("cart.api.urls")),
    path('api/discount/',include("discount.api.urls")),

    #password reset and change
    path('password_change/done',auth_views.PasswordChangeDoneView.as_view(template_name='password_change_done.html'),name='password_change_done'),
   
    path('password_change/',auth_views.PasswordChangeView.as_view(template_name='password_change.html'),name='password_change'),

    path('password_reset/done',auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_done.html'),name='password_reset_done'),
    
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='password_reset_form.html'), name='password_reset'),

    path('reset/done',auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),name='password_reset_complete'),
    
    # url(r'^api/v1/account/', include(('rest_accounts.urls', 'restprofile'), namespace='rest_accounts')),
    
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)




