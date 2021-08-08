from django.urls import path,include
from .import views
# from rest_framework import routers
# router = routers.SimpleRouter()
# router.register(r'users', views.CustomUserViewSet)

urlpatterns = [ 
   
    path('login', views.dologin,name='dologin'),
    path('singup', views.dosingup.as_view(),name='dosingup'),
    path('instructor_singup', views.instructor_singup,name='instructor_singup'),
    path('customer_singup', views.customer_singup,name='customer_singup'),
    path('counsellor_singup', views.counsellor_singup,name='counsellor_singup'),
    # path('selection', views.selection,name='selection'),
    path('selection', views.selection,name='selection'),
    path('activate/<uidb64>/<token>', views.activate,name='activate'),
    # path('apitest', include(router.urls)), 
    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))

]