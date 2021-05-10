from django.urls import path
from .import views

urlpatterns = [
    path('', views.counsellor_dashboard,name='counsellor_dashboard'),
    path('manage_staff', views.manage_staff,name='manage_staff'),
    path('staff_activate/<id>', views.staff_activate,name='staff_activate'),
    path('staff_deactivate/<id>', views.staff_deactivate,name='staff_deactivate'),

    path('manage_customer', views.manage_customer,name='manage_customer'),
    path('customer_activate/<id>', views.customer_activate,name='customer_activate'),
    path('customer_deactivate/<id>', views.customer_deactivate,name='customer_deactivate'),

    path('product_activate/<slug>', views.product_activate,name='product_activate'),
    path('product_deactivate/<slug>', views.product_deactivate,name='product_deactivate'),
    path('manage_product', views.manage_product,name='manage_customer'),
    path('check_product_session_activate/<slug>/<sslug>/<ssslug>', views.check_product_session_activate,name='check_product_session_activate'),
    path('check_product_session_deactivate/<slug>/<sslug>/<ssslug>', views.check_product_session_deactivate,name='check_product_session_deactivate'),
    
    path('product_category', views.product_category,name='product_category'),
    path('product_subcategory/<id>', views.product_subcategory,name='product_subcategory'),
    path('product_category_delete/<id>', views.product_category_delete,name='product_category_delete'),
    path('product_subcategory_delete/<sid>/<id>', views.product_subcategory_delete,name='product_subcategory_delete'),

    path('check_product_details/<slug>', views.check_product_details,name='check_product_details'),
    path('check_product_session/<slug>/<sslug>/<ssslug>', views.check_product_session,name='check_product_session'),

    path('counsellor_login', views.counsellor_login,name='counsellor_login'),
    # path('counsellor_singup', views.counsellor_singup,name='counsellor_singup'),
    path('counsellor_logout', views.counsellor_logout,name='counsellor_logout')
]