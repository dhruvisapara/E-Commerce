from django.urls import include, path
from rest_framework import routers
from payments.views import PymentViewSet

router = routers.SimpleRouter()
router.register(r'payment',PymentViewSet, basename="payment")

urlpatterns = [

    path('', include(router.urls))
]
