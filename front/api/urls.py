from front.api import views
from django.urls import path
from rest_framework.authtoken import views as authviews


urlpatterns = [
    path('<slug>/',views.api_detail_product_view,name="detail"),
    path('module/<id>/',views.ApiProductModuleListView.as_view(),name="moduleslist"),
    path('create',views.api_create_product_view,name="create"),
    path('<slug>/delete',views.api_delete_product_view,name="delete"),
    path('<slug>/update',views.api_update_product_view,name="update"),
    # path('list',views.ApiProductListView.as_view(),name="list"),
    path('<slug>/is_teacher',views.api_is_teacher_of_product,name="is_teacher"),

    #new API
    path('product_category',views.ApiCategoriesListView.as_view(),name="product_category"),
    path('product_category/<id>',views.ApiCategoriesListView.as_view(),name="product_category"),
    path('product_subcategory',views.ApiSubCategoriesListView.as_view(),name="product_subcategory"),
    path('product_subcategory/<id>',views.ApiSubCategoriesListView.as_view(),name="product_subcategory"),
    path('product_childsubcategory',views.ApiChildCategoriesListView.as_view(),name="product_childsubcategory"),
    path('product_childsubcategory/<id>',views.ApiChildCategoriesListView.as_view(),name="product_childsubcategory"),
    path('product_details/<id>',views.ApiProductDtailsListView.as_view(),name="product_details"),
    # path('product_subcategory/<id>',views.ApiSubCategoriesListView.as_view(),name="product_category"),
    
]