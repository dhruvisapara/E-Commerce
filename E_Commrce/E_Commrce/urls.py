"""E_Commrce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path, re_path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny

API_PREFIX = '<version>(v1)'
schema_view = get_schema_view(
    openapi.Info(
        title="E_COMMERCE API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[AllowAny],
)

urlpatterns = [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    # path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # # Optional UI:
    # path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    # path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

# urlpatterns += [
#     re_path(r"^api/(?P<version>(v1|v2))/", include('category.urls')),
#     re_path(r"^api/(?P<version>(v1|v2))/", include('customer.urls')),
#     re_path(r"^api/(?P<version>(v1|v2))/", include('products.urls')),
#     # re_path(r"^api/(?P<version>(v1|v2))/", include('cart.urls')),
#     re_path(r"^api/(?P<version>(v1|v2))/", include('order.urls')),
#     re_path(r"^api/(?P<version>(v1|v2))/", include('address.urls')),
#     re_path(r"^api/(?P<version>(v1|v2))/", include('tag.urls')),
# ]

urlpatterns += [

    ################## admin url ##################################
    path('admin/', admin.site.urls),

    # ################## custom app urls #############################
    #
    re_path(r"^api/(?P<version>(v1|v2))/", include('category.urls')),
    re_path(r"^api/(?P<version>(v1|v2))/", include('customer.urls')),
    re_path(r"^api/(?P<version>(v1|v2))/", include('products.urls')),
    # re_path(r"^api/(?P<version>(v1|v2))/", include('cart.urls')),
    re_path(r"^api/(?P<version>(v1|v2))/", include('order.urls')),
    re_path(r"^api/(?P<version>(v1|v2))/", include('address.urls')),
    # re_path(r"^api/(?P<version>(v1|v2))/", include('tag.urls')),
    #
    # path('api/v1/', include('customer.urls')),
    # path('api/v1/', include('category.urls')),
    # path("api/v1/", include('products.urls')),
    path("api/v1/", include('cart.urls')),
    # # re_path(r'^i18n/', include('django.conf.urls.i18n')),
    # path("api/v1/", include('order.urls')),
    # path("api/v1/", include('address.urls')),
    # path("api/v1/", include('tag.urls')),

]
