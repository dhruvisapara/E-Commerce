from django.urls import path, include
from rest_framework import routers

from address.views import UserAddress

router = routers.SimpleRouter()
router.register(r'address', UserAddress, basename="address")
urlpatterns = [
    path('', include(router.urls))]