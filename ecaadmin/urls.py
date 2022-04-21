from django.urls import path
from ecaadmin import views

urlpatterns = [
    path('', views.admin_home,name='admin_home'),    
    # path('category_list', views.ProductCategoryListViews.as_view(),name='category_list'),
    path('category_list', views.ProductCategoryTabListViews.as_view(),name='category_tab_list'),
    path('category_active/<slug:pk>', views.activeCategory,name='category_active'),
    path('category_deactive/<slug:pk>', views.deactiveCategory,name='category_deactive'),
    path('category_create', views.ProductCategoryCreate.as_view(),name='category_create'),
    path('category_update/<slug:pk>', views.ProductCategoryUpdate.as_view(),name='category_update'),
    
    path('delete_category', views.DeleteAll,name='delete_category'),

    
    path('subcategory_list1', views.ProductSubCategoryListViews.as_view(),name='subcategory_list'),
    path('subcategory_list', views.ProductSubCategoryTabListViews.as_view(),name='subcategory_tab_list'),
    path('subcategory_active/<slug:pk>', views.activeSubCategory,name='subcategory_active'),
    path('subcategory_deactive/<slug:pk>', views.deactiveSubCategory,name='subcategory_deactive'),
    path('subcategory_create', views.ProductSubCategoryCreate.as_view(),name='subcategory_create'),
    path('subcategory_update/<slug:pk>', views.ProductSubCategoryUpdate.as_view(),name='subcategory_update'),
    
    path('childsubcategory_list', views.ProductChildSubCategoryListViews.as_view(),name='childsubcategory_list'),
    path('childsubcategory_tab_list', views.ProductChildSubCategoryTabListViews.as_view(),name='childsubcategory_tab_list'),
    path('childsubcategory_active/<slug:pk>', views.activeChildSubCategory,name='childsubcategory_active'),
    path('childsubcategory_deactive/<slug:pk>', views.deactiveChildSubCategory,name='childsubcategory_deactive'),
    path('childsubcategory_create', views.ProductChildSubCategoryCreate.as_view(),name='childsubcategory_create'),
    path('childsubcategory_update/<slug:pk>', views.ProductChildSubCategoryUpdate.as_view(),name='childsubcategory_update'),
    
    # Merchant
    path('merchant_list', views.MerchantUserListViews.as_view(),name='merchant_list'),
    path('merchant_tab_list', views.MerchantUserTabListViews.as_view(),name='merchant_tab_list'),
    path('merchant_active/<slug:pk>', views.activeMerchant,name='merchant_active'),
    path('merchant_deactive/<slug:pk>', views.deactiveMerchant,name='merchant_deactive'),
    path('merchant_create', views.MerchantUserCreateView.as_view(),name='merchant_create'),
    path('merchant_update/<slug:pk>', views.MerchantUserUpdate.as_view(),name='merchant_update'),
    
    # Product
    path('product_list', views.ProductListViews.as_view(),name='product_list'),
    path('product_tab_list', views.ProductTabListViews.as_view(),name='product_tab_list'),
    path('product_create', views.ProductView.as_view(),name='product_view'),
    path('add_product', views.AddProductView.as_view(),name='add_product'),
    path('product_active/<slug:pk>', views.activeProduct,name='product_active'),
    path('product_deactive/<slug:pk>', views.deactiveProduct,name='product_deactive'),
    path('product_update/<str:product_id>', views.ProductUpdate.as_view(),name='product_update'),
    path('product_new_update/<str:product_id>', views.ProductNewUpdate.as_view(),name='product_new_update'),
    path('product_add_media/<str:product_id>', views.ProductAddMedia.as_view(),name='product_add_media'),
    path('product_edit_media/<str:product_id>',views.ProductEditMedia.as_view(),name="product_edit_media"),
    path('product_media_delete/<str:id>',views.ProductMediaDelete.as_view(),name="product_media_delete"),
    path('product_add_stocks/<str:product_id>',views.ProductAddStocks.as_view(),name="product_add_stocks"),
    path('file_upload', views.file_upload,name='file_upload'),

    #Add Exlusive products
    path('add_exclusive',views.AddExclusive,name="add_exclusive"),

    #Coupons List, Add ,delete
    path('add_delivery_cost',views.DeliveryCostView.as_view(),name="add_delivery_cost"),
    path('delete__delivery_cost/<id>',views.deleteDeliveryCostView,name="delete__delivery_cost"),

    #order list
    path('order_list',views.OrderListView.as_view(),name="order_list"),
    path('admin_order_details/<id>',views.OrderDetailView.as_view(),name="admin_order_details"),
    path('admin_order_update/<id>',views.OrderUpdateView.as_view(),name="admin_order_update"),
    path('admin_order_print/<id>',views.adminOrderPrint,name="admin_order_print"),
    path('admin_shipping_print/<id>',views.adminShippingPrint,name="admin_shipping_print"),


    #Staff User
    path('staff_create',views.StaffUserCreateView.as_view(),name="staff_create"),
    path('staff_list',views.StaffUserListView.as_view(),name="staff_list"),
    path('staff_update/<slug:pk>',views.StaffUserUpdateView.as_view(),name="staff_update"),

    #GST Details
    path('gst_create',views.GstCreateView.as_view(),name="gst_create"),
    path('gst_delete/<slug:pk>',views.gstDelete,name="gst_delete"),

    #Customer User
    path('customer_create',views.CustomerUserCreateView.as_view(),name="customer_create"),
    path('customer_list',views.CustomerUserListView.as_view(),name="customer_list"),
    path('customer_update/<slug:pk>',views.CustomerUserUpdateView.as_view(),name="customer_update"),

]