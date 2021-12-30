from front.api import views
from django.urls import path
from rest_framework.authtoken import views as authviews


urlpatterns = [

    #new API
    path('product_category',views.ApiCategoriesListView.as_view()),
    path('product_category/<id>',views.ApiCategoriesListView.as_view()),
    path('product_subcategory',views.ApiSubCategoriesListView.as_view()),
    path('product_subcategory/<id>',views.ApiSubCategoriesListView.as_view()),
    path('product_childsubcategory',views.ApiChildCategoriesListView.as_view()),
    path('product_childsubcategory/<id>',views.ApiChildCategoriesListView.as_view()),
    path('product_details/<id>',views.ApiProductDtailsListView.as_view()),
    # path('product_subcategory/<id>',views.ApiSubCategoriesListView.as_view(),name="product_category"),
    
]