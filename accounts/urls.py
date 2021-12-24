from django.urls import path,include
from .import views
# from rest_framework import routers
# router = routers.SimpleRouter()
# router.register(r'users', views.CustomUserViewSet)

urlpatterns = [ 
   
    path('login', views.dologin,name='dologin'),
    path('singup', views.dosingup.as_view(),name='dosingup'),
    path('customer_singup', views.customer_singup,name='customer_singup'),
    path("verifyOTP/<phone>", views.verifyOTP, name="OTP_Gen"),
    path("verifyPhone/<phone>", views.verifyPhone, name="verifyPhone"),
    path("resendOTP/<phone>", views.resendOTP, name="resendOTP"),
    path('Authorizedsingup', views.AuthorizedSingup.as_view(),name='Authorizedsingup'),
    path('activate/<uidb64>/<token>', views.activate,name='activate'),
    # path('apitest', include(router.urls)), 
    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))

]