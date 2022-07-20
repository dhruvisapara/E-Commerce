from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView, TokenVerifyView)

from customer.views import (BusinessViewSet, RegisterStaffViewSet,
                            Registration, StaffProfileViewSet, Userlist)

router = routers.SimpleRouter()
router.register(r'register', Registration, basename="register")
router.register(r'business_register', BusinessViewSet, basename="business_register")
router.register(r'staff_register', RegisterStaffViewSet, basename="staff_register")

urlpatterns = [
    path('', include(router.urls)),
    path('get_token/', TokenObtainPairView.as_view(), name='get_token'),
    path('refresh_token/', TokenRefreshView.as_view(), name='refresh_token'),
    path('verify_token/', TokenVerifyView.as_view(), name='verify_token'),
    path('current-user/', Userlist.as_view(), name='current-user'),
    path('staff_list/', StaffProfileViewSet.as_view(), name='staff_list'),

]
