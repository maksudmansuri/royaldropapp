from front.api import views
from django.conf.urls import url
from django.urls import path
from rest_framework.authtoken import views as authviews


urlpatterns = [
    path('<slug>/',views.api_detail_product_view,name="detail"),
    path('create',views.api_create_product_view,name="create"),
    path('<slug>/delete',views.api_delete_product_view,name="delete"),
    path('<slug>/update',views.api_update_product_view,name="update"),
    path('list',views.ApiProductListView.as_view(),name="list"),
    path('<slug>/is_teacher',views.api_is_teacher_of_product,name="is_teacher"),

    
]