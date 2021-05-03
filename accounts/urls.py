# from django.contrib import admin
from django.urls import path
from knox import views as knox_views
from .views import *

urlpatterns = [
    # path('admin/', admin.site.urls),
    # path('', views.index, name="home"),
    path('validatePhone/', ValidatePhoneSendOTP.as_view()),
    path('validateotp/', ValidateOTP.as_view()),
    path('register/', Register.as_view()),
    path('login/', ObtainAuthTokenView.as_view()),
    # path('logout/', Logout.as_view()),
    # path('dologout', dologout),


]