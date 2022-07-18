from django.urls import path, include
from rest_framework import routers
from category.views import CategoryView, CategoryValidationView

router = routers.SimpleRouter()
router.register(r'category', CategoryView, basename="category")


urlpatterns = [

    path('', include(router.urls)),
    path('category_validation/',CategoryValidationView.as_view(),name="category_validation")
]
