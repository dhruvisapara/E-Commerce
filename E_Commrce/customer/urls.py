from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from customer.views import Registration, Userlist

router = routers.SimpleRouter()
router.register(r'register', Registration, basename="register")

urlpatterns = [
    path('', include(router.urls)),
    path('get_token/', TokenObtainPairView.as_view(), name='get_token'),
    path('refresh_token/', TokenRefreshView.as_view(), name='refresh_token'),
    path('verify_token/', TokenVerifyView.as_view(), name='verify_token'),
    path('current-user/', Userlist.as_view(), name='current-user'),

]
