from django.urls import path
from django.conf import settings
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

app_name = "healthapp"
urlpatterns = [
    path('', views.data_list),
    path('<int:id>', views.drink_detail)
]
urlpatterns = format_suffix_patterns(urlpatterns)