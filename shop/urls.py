from django.urls import path, re_path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from rest_framework.urlpatterns import format_suffix_patterns
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from . import views

app_name = "shop"
urlpatterns = [
   path("", views.index, name="index"),
   re_path(r'^(?P<product_slug>[\w-]+)-a(?P<product_id>\d+)\.html$',
         views.product, name='product'),
   path("blog-<slug:blog_slug>-b<int:blog_id>.html", views.blog, name='blog'),
   path("shop.html", views.category, name="shop"),
   path("cart.html", views.cart, name="cart"),
   path("add-to-cart.html", views.add_to_cart, name="add_to_cart"),
   path("update-cart.html", views.update_cart, name="update_cart"),
   path("checkout.html", views.checkout, name="checkout"),
   path("notify.html", views.success, name="success"),
   path("contact.html", views.contact, name="contact"),
   path("check-order.html", views.check_order, name="check_order"),
   path("<slug:category_slug>.html", views.category, name="category"),

   # API_DOCUMENTATIONS
   path('categories/', views.ShopCategoryListCreateAPIView.as_view(),
      name='shop_category_list_create'),
   path('categories/<int:id>/', views.ShopCategoryRetrieveUpdateDestroyAPIView.as_view(),
      name='shop_category_retrieve_update_destroy_id'),
   path('categories/<slug:slug>/', views.ShopCategoryRetrieveUpdateDestroyAPIView.as_view(),
      name='shop_category_retrieve_update_destroy_slug'),

   path('products/', views.ShopProductListCreateAPIView.as_view(),
      name='shop_product_list_create'),
   path('products/<int:id>/', views.ShopProductRetrieveUpdateDestroyAPIView.as_view(),
      name='shop_product_retrieve_update_destroy_id'),
   path('products/<slug:slug>/', views.ShopProductRetrieveUpdateDestroyAPIView.as_view(),
      name='shop_product_retrieve_update_destroy_slug'),

   path('blogs/', views.ShopBlogListCreateAPIView.as_view(),
      name='shop_blog_list_create'),
   path('blogs/<int:id>/', views.ShopBlogRetrieveUpdateDestroyAPIView.as_view(),
      name='shop_blog_retrieve_update_destroy_id'),
   path('blogs/<slug:slug>/', views.ShopBlogRetrieveUpdateDestroyAPIView.as_view(),
      name='shop_blog_retrieve_update_destroy_slug'),

   path('plantingmethods/', views.ShopPlantingMethodListCreateAPIView.as_view(),
      name='shop_plantingmethods_list_create'),
   path('plantingmethods/<int:id>/', views.ShopPlantingMethodRetrieveUpdateDestroyAPIView.as_view(),
      name='shop_plantingmethods_retrieve_update_destroy_id'),
   path('plantingmethods/<slug:slug>/', views.ShopPlantingMethodRetrieveUpdateDestroyAPIView.as_view(),
      name='shop_plantingmethods_retrieve_update_destroy_slug'),
]

if settings.DEBUG:  # loading static files
   urlpatterns += static(settings.MEDIA_URL,
                        document_root=settings.MEDIA_ROOT)
   urlpatterns += static(settings.STATIC_URL,
                        document_root=settings.STATIC_ROOT)
