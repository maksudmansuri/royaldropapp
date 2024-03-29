from django.urls import path
from .import views,orderviews
from django.contrib.auth.decorators import login_required

urlpatterns = [ 
    #for session stored
    path('basket_add', views.basket_add,name='basket_add'),
    path('basket_delete', views.basket_delete,name='basket_delete'),

    path('home2', views.indexView.as_view(),name='home2'),
    # path('', views.index,name='home'),
    path('home_two', views.home_two,name='home_two'),
    path('base', views.baseView.as_view(),name='base'),
    path('', views.HomeListview.as_view(),name='home'),
 
    # path('home_two', views.home_two,name='home_two'),
    path('product_list', views.Product_list,name='product_list'),
    path('product_filter_list', views.ProductFilterListView.as_view(),name='product_filter_list'),
    path('testing_file', views.testing_file,name='testing_file'),  
    # path('testing_file', views.testing_file,name='testing_file'),
    path('product_details/<slug:product_slug>', views.ProductDetailView.as_view(),name='product_details'),
    path('checkout',views.CheckoutListView.as_view(),name='checkout'),
    path('paymenthandler/',views.paymenthandler,name='paymenthandler'),
    path('razorpay',views.RazorpayPayment,name='razorpay'),

    path('add-to-cart', views.AddUpdateCart,name='add-to-cart'), 
    path('cart', views.CartListView.as_view(),name='cart'), 
    path('product_details_2', views.Product_details_2,name='product_details_2'),
    # path('product_details_2', views.Product_details_2,name='product_details_2'),
    # path('instructor_singup', views.instructor_singup,name='instructor_singup'),
    # path('instructor_logout', views.instructor_logout,name='instructor_logout'),
    path('logout', views.dologout,name='dologout'),
    path('about_us', views.about_us,name='about_us'),
    path('career', views.career,name='career'),
    path('contact_us', views.contact_us,name='contact_us'),
       
    # For user login deatils
    path('dashboard',orderviews.dashboardView.as_view(),name='dashboard'),
    path('dash_my_profile',orderviews.dashMyProfileView.as_view(),name='dash_my_profile'),
    path('dash_edit_profile',orderviews.dashEditProfileUpdateView.as_view(),name='dash_edit_profile'),

    #user Address details 
    path('dash_address_book',orderviews.dashAddressBookView.as_view(),name='dash_address_book'),
    path('dash_address_make_default',orderviews.dashAddressMakeDefaultView.as_view(),name='dash_address_make_default'),
    path('dash_address_add',orderviews.dashAddressAddView.as_view(),name='dash_address_add'),
    path('checkoutdeafaultaddresschange',orderviews.checkoutDefaultAddresschangeView.as_view(),name='checkoutdeafaultaddresschange'),
    path('checoutAddressAdd',orderviews.checoutAddressAddView.as_view(),name='checoutAddressAdd'),
    path('dash_address_edit/<slug:pk>',orderviews.dashAddressUpdateView.as_view(),name='dash_address_edit'),
    # path('dash_track_order/<slug:pk>',orderviews.dashTrackOrderView.as_view(),name='dash_track_order'),
    path('dash_my_order',orderviews.dashMyOrderView.as_view(),name='dash_my_order'),
    path('dash_my_order_detial',orderviews.dashMyOrderDetailView.as_view(),name='dash_my_order_detial'),
    path('dash_track_order',orderviews.dashTrackOrderView.as_view(),name='dash_track_order'),
    path('dash_track_order_by_tracker/<slug:pk>',orderviews.dashTrackOrderByTrackerView.as_view(),name='dash_track_order_by_tracker'),
    path('dash_manage_order',orderviews.dashManageOrderView.as_view(),name='dash_manage_order'),
    path('dash_payment_option',orderviews.dashPaymentOptionView.as_view(),name='dash_payment_option'),
    path('dash_cancellation',orderviews.dashCancellationView.as_view(),name='dash_cancellation'),

]
