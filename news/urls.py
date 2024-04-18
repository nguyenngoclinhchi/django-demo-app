from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from . import views

app_name = 'news'
urlpatterns = [
    path('', views.index, name='index'),
    path('tinymce/', include('tinymce.urls')),
    # path('post/<slug:post_slug>', views.post, name='post'),
    # path('feed/<slug:feed_slug>', views.feed, name='feed'),
    re_path(r'^(?P<post_slug>[\w-]+)-a(?P<post_id>\d+)\.html$', views.post, name='post'),
    re_path(r'^tin-tuc-tong-hop-(?P<feed_slug>[\w-]+)\.html$', views.feed, name='feed'),
    path('search.html', views.search, name='search'),
    path('about.html', views.about, name='about'),
    path('contact.html', views.contact, name='contact'),
    path('<slug:category_slug>.html', views.category, name='category'),

    # API_DOCUMENTATIONS
    path('articles/', views.ArticleListCreateAPIView.as_view(), name='news_article_list_create'),
    path('articles/<int:id>/', views.ArticleRetrieveUpdateDestroyAPIView.as_view(), name='news_article_retrieve_update_destroy_id'),
    path('articles/<slug:slug>/', views.ArticleRetrieveUpdateDestroyAPIView.as_view(), name='news_article_retrieve_update_destroy_slug'),

    # http://127.0.0.1:8000/news/articles-for-user/?username=admin123
    path('articles/for-user/', views.ListArticlesForAuthor.as_view(), name='news_articles_filter_based_user'),
    path('articles/per-user-link/', views.get_articles_for_current_user_related_links, name='news_articles_list_user_retrieve_links'),
    path('articles/per-user-string/', views.get_articles_for_current_user_strings, name='news_articles_list_user_retrieve_strings'),

    path('categories/', views.CategoryListCreateAPIView.as_view(), name='news_category_list_create'),
    path('categories/<int:id>/', views.CategoryRetrieveUpdateDestroyAPIView.as_view(), name='news_category_retrieve_update_destroy_id'),
    path('categories/<slug:slug>/', views.CategoryRetrieveUpdateDestroyAPIView.as_view(), name='news_category_retrieve_update_destroy_slug'),

    path('feeds/', views.FeedListCreateAPIView.as_view(), name='news_feed_list_create'),
    path('feeds/<int:id>/', views.FeedRetrieveUpdateDestroyAPIView.as_view(), name='news_feed_retrieve_update_destroy_id'),
    path('feeds/<slug:slug>/', views.FeedRetrieveUpdateDestroyAPIView.as_view(), name='news_feed_retrieve_update_destroy_slug'),
]
if settings.DEBUG: # loading static files
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
    urlpatterns+=static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)