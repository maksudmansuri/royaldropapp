from django.urls import path
from ecaadmin import views

urlpatterns = [
    path('home', views.admin_home,name='admin_home'),
    path('category_list', views.CategoriesListViews.as_view(),name='category_list'),
    path('categori_create', views.CategoriesCreateView.as_view(),name='category_create'),
    

]