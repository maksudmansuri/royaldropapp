from django.urls import path
from .import views

urlpatterns = [
    path('home2', views.indexView.as_view(),name='home2'),
    # path('', views.index,name='home'),
    path('home_two', views.home_two,name='home_two'),
    path('', views.home2.as_view(),name='home'),

    # path('home_two', views.home_two,name='home_two'),
    path('product_list', views.Product_list,name='product_list'),
    # path('product_list', views.Product_list,name='product_list'),
    path('testing_file', views.testing_file,name='testing_file'),
    # path('testing_file', views.testing_file,name='testing_file'),
    path('product_details/<slug:slug>', views.Product_details,name='product_details'),
    # path('product_details/<slug:slug>', views.Product_details,name='product_details'),
    path('product_details_2', views.Product_details_2,name='product_details_2'),
    # path('product_details_2', views.Product_details_2,name='product_details_2'),
    # path('instructor_singup', views.instructor_singup,name='instructor_singup'),
    # path('instructor_logout', views.instructor_logout,name='instructor_logout'),
    path('logout', views.dologout,name='dologout'),
    path('about_us', views.about_us,name='about_us'),
    path('career', views.career,name='career'),
    path('contact_us', views.contact_us,name='contact_us'),
]
