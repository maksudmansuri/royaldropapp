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
    path('login/', LoginAPI.as_view()),
    path('logout/$', knox_views.LogoutView.as_view()),


]