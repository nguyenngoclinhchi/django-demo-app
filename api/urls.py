from django.urls import path, re_path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from rest_framework.urlpatterns import format_suffix_patterns
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from . import views

app_name = "api"
urlpatterns = [
    path("products/category/<int:category_id>/",
         views.ProductCategoryApiView.as_view(), name="product-category"),
    path("products/related/<int:product_id>/",
         views.ProductRelatedApiView.as_view(), name="product-related"),

]
