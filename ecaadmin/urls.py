from django.urls import path
from ecaadmin import views

urlpatterns = [
    path('home', views.admin_home,name='admin_home'),
    path('category_list', views.ProductCategoryListViews.as_view(),name='category_list'),
    path('category_create', views.ProductCategoryCreate.as_view(),name='category_create'),
    path('category_update/<slug:pk>', views.ProductCategoryUpdate.as_view(),name='category_update'),
    

]