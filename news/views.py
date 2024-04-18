from bs4 import BeautifulSoup
from re import escape

from django.shortcuts import get_object_or_404, render
from django.core.paginator import Paginator
from django.utils import timezone

from rest_framework import generics, mixins, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import (
    IsAuthenticated,
    AllowAny,
    IsAuthenticatedOrReadOnly,
    IsAdminUser,
)
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from account.serializers import CurrentUserArticlesRelatedLinksSerializer, CurrentUserArticlesStringsSerializer
from .permissions import AuthorOrReadOnly
from .api_view_helpers import ListCreateAPIViewBase, RetrieveUpdateDestroyAPIViewBase
from .serializers import ArticleSerializer, CategorySerializer, FeedSerializer
from .define import *
from .models import Article, Category, Feed
import feedparser

def index(request):
    items_article_special = Article.objects.filter(
        special=True,
        status=APP_VALUE_STATUS_ACTIVE,
        publish_date__lte =timezone.now()).order_by('-publish_date')
    
    items_category = Category.objects.filter(
        status=APP_VALUE_STATUS_ACTIVE,
        is_homepage=True).order_by('ordering')
    
    for category in items_category: 
        category.article_filter = category.article_set.filter(
            status=APP_VALUE_STATUS_ACTIVE,
            publish_date__lte =timezone.now()).order_by('-publish_date')
        
    return render(request, APP_PATH_PAGE + 'index.html', {
        "title_page": "Homepage",
        "items_article_special": items_article_special[:SETTINGS_ITEM_ARTICLE_SPECIAL],
        "items_category": items_category
    })

def category(request, category_slug):
    # category_slug --> retrieve category info 
    # --> articles belonging to category --> display on client-side
    # retrieve data from database, else 404
    item_category = get_object_or_404(
        Category,
        slug=category_slug, 
        status=APP_VALUE_STATUS_ACTIVE)

    # category=item_category NOT category_slug
    # ordering descending add -, else increasing
    items_article = Article.objects.filter(
        category=item_category,
        status=APP_VALUE_STATUS_ACTIVE,
        publish_date__lte =timezone.now()).order_by('-publish_date')

    # if the page request > available page, it will shows the last page
    paginator = Paginator(items_article, per_page=SETTINGS_ARTICLE_NUMBER_PER_PAGE)
    page = request.GET.get('page')
    items_article = paginator.get_page(page) 
    
    # after I get item_category, I will pass to the views
    return render(request, APP_PATH_PAGE + 'category.html', {
        "title_page": item_category.name,
        "item_category": item_category,
        "items_article": items_article, # current page is stored on items_article.number
        "paginator": paginator
    })

def post(request, post_slug, post_id):
    item_post = get_object_or_404(
        Article,
        slug=post_slug, 
        id=post_id,
        status=APP_VALUE_STATUS_ACTIVE,
        publish_date__lte =timezone.now())

    items_article_related = Article.objects.filter(
        category=item_post.category,
        status=APP_VALUE_STATUS_ACTIVE,
        publish_date__lte = timezone.now()).order_by('-publish_date').exclude(slug=item_post.slug)[:SETTINGS_ITEMS_ARTICLE_RELATED]

    return render(request, APP_PATH_PAGE + 'post.html', {
        "title_page": item_post.name,
        "item_post": item_post,
        "items_article_related": items_article_related
    })

def feed(request, feed_slug):
    item_feed = get_object_or_404(
        Feed,
        slug=feed_slug, 
        status=APP_VALUE_STATUS_ACTIVE)
    
    items_feed = []
    try: 
        feed = feedparser.parse(item_feed.link)
        # with open('feed.json', 'w', encoding='utf-8') as f:
        #     json.dump(feed, f, ensure_ascii=False)
        for entry in feed.entries: 
            soup = BeautifulSoup(entry.summary, 'html.parser')
            img_tag = soup.find('img')
            src_img = img_tag['src'] if img_tag else APP_VALUE_IMG_DEFAULT
            item = {
                'title': entry.title,
                'link': entry.link,
                'pub_date': entry.published,
                'img': src_img
            }
            items_feed.append(item)
    except: 
        print("GET_FEED: ERROR!")

    return render(request, APP_PATH_PAGE + 'feed.html', {
        "title_page": SETTINGS_FEED_TITLE_PAGE_MESSAGE + item_feed.name,
        "item_feed": item_feed,
        "items_feed": items_feed
    })

def search(request):
    keyword = request.GET.get('keyword')
    items_article = Article.objects.filter(
        # regular expression, iregex = in-case-sensitive regular regex
        name__iregex = escape(keyword),
        status=APP_VALUE_STATUS_ACTIVE,
        publish_date__lte =timezone.now()).order_by('-publish_date')
    paginator = Paginator(items_article, per_page=SETTINGS_ARTICLE_NUMBER_PER_PAGE)
    page = request.GET.get('page')
    items_article = paginator.get_page(page) 

    return render(request, APP_PATH_PAGE + 'search.html', {
        "title_page": "Searching for keyword: " + keyword,
        "keyword": keyword,
        "items_article": items_article,
        "paginator": paginator
    })

def about(request): 
    return render(request, APP_PATH_PAGE + 'about.html', {
        "title_page": "Introduction"
    })

def contact(request): 
    return render(request, APP_PATH_PAGE + 'contact.html', {
        "title_page": "Contact"
    })

# -------------------------------- API DOCUMENTATION ------------------------------
class ArticleListCreateAPIView(ListCreateAPIViewBase):
    serializer_class = ArticleSerializer
    model_class = Article
    permission_classes = [IsAuthenticated]

# only author allow to change the article
class ArticleRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIViewBase):
    serializer_class = ArticleSerializer
    model_class = Article
    permission_classes = [IsAuthenticated, AuthorOrReadOnly]

class CategoryListCreateAPIView(ListCreateAPIViewBase):
    serializer_class = CategorySerializer
    model_class = Category
    permission_classes = [IsAuthenticated]

class CategoryRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIViewBase):
    serializer_class = CategorySerializer
    model_class = Category
    permission_classes = [IsAuthenticated]

class FeedListCreateAPIView(ListCreateAPIViewBase):
    serializer_class = FeedSerializer
    model_class = Feed
    permission_classes = [IsAuthenticated]

class FeedRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIViewBase):
    serializer_class = FeedSerializer
    model_class = Feed
    permission_classes = [IsAuthenticated]

# list out all articles with username = author username, no need to be author
class ListArticlesForAuthor(ListCreateAPIViewBase):
    model_class = Article
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticated]
    queryset = Article.objects.all()

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'username', 
                openapi.IN_QUERY, 
                description='Filter articles by username', 
                type=openapi.TYPE_STRING,
                required=False
            )
        ]
    )
    def get_queryset(self):
        username = self.request.query_params.get("username")
        if username:
            self.queryset = self.queryset.filter(author__username=username)
        return self.queryset

@api_view(http_method_names=["GET"])
@permission_classes([IsAuthenticated])
def get_articles_for_current_user_related_links(request: Request):
    user = request.user
    serializer = CurrentUserArticlesRelatedLinksSerializer(
        instance=user, context={"request": request}
    )
    return Response(data=serializer.data, status=status.HTTP_200_OK)

@api_view(http_method_names=["GET"])
@permission_classes([IsAuthenticated])
def get_articles_for_current_user_strings(request: Request):
    user = request.user
    serializer = CurrentUserArticlesStringsSerializer(
        instance=user, context={"request": request}
    )
    return Response(data=serializer.data, status=status.HTTP_200_OK)
