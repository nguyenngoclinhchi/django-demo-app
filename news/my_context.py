from django.utils import timezone
import requests

from .helpers import get_skip_path_slug_article
from .define import *
from .models import Article, Category, Feed
from django.db.models import Count
import json

def items_category_sidebar_menu(request): 
    items_category_sidebar_menu = Category.objects.filter(
        status=APP_VALUE_STATUS_ACTIVE).order_by('ordering').annotate(num_articles=Count('article'))[:SETTINGS_CATEGORY_TOTAL_ITEMS_SIDEBAR]
    return {"items_category_sidebar_menu": items_category_sidebar_menu}

def items_feed_sidebar_menu(request): 
    items_feed_sidebar_menu = Feed.objects.filter(
        status=APP_VALUE_STATUS_ACTIVE).order_by('ordering')[:SETTINGS_FEED_TOTAL_ITEMS_SIDEBAR]
    return {"items_feed_sidebar_menu": items_feed_sidebar_menu}

def items_article_recent_sidebar_menu(request): 
    # cannot get request.get_path() --> have to check later
    skip_slug = get_skip_path_slug_article(request.get_full_path())
    # /post/mai-movie-ranks-16th-at-worldwide-box-office if at the current article?page=2
    # skip_slug = request.get_full_path().replace("/post/", "")
    items_article_recent_sidebar_menu =  Article.objects.filter(
        status=APP_VALUE_STATUS_ACTIVE,
        publish_date__lte =timezone.now()).order_by('-publish_date').exclude(slug=skip_slug)[:SETTINGS_ITEMS_ARTICLE_RECENT]
    return {
        "items_article_recent_sidebar_menu": items_article_recent_sidebar_menu
    }

def items_article_footer_random_sidebar_menu(request): 
    skip_slug = get_skip_path_slug_article(request.get_full_path())
    items_article_footer_random_sidebar_menu =  Article.objects.filter(
        status=APP_VALUE_STATUS_ACTIVE,
        # order_by('?') refers to random
        publish_date__lte =timezone.now()).order_by('?').exclude(slug=skip_slug)[:SETTINGS_ITEM_ARTICLE_RANDOM]
    return {
        "items_article_footer_random_sidebar_menu": items_article_footer_random_sidebar_menu
    }

def items_article_header_trending(request): 
    skip_slug = get_skip_path_slug_article(request.get_full_path())
    items_article_header_trending =  Article.objects.filter(
        status=APP_VALUE_STATUS_ACTIVE,
        # order_by('?') refers to random
        publish_date__lte =timezone.now()).order_by('?').exclude(slug=skip_slug)
    return {
        "items_article_header_trending": items_article_header_trending
    }

def items_price_sidebar_coin(request): 
    url = SETTINGS_API_PRICE_COIN_URL
    items_price_sidebar_coin = []
    try: 
        response = requests.get(url)
        if (response.status_code == HTTP_STATUS_SUCCESS): 
            items_price_sidebar_coin = response.json()[:SETTINGS_ITEM_PRICE_COIN]
    except: 
        print("GET_COIN: ERROR!")
    # with open('coin.json', 'w', encoding='utf-8') as f:
    #     json.dump(items_price_sidebar_coin, f, ensure_ascii=False)
    # print(items_price_sidebar_coin)
    return {
        "items_price_sidebar_coin": items_price_sidebar_coin
    }

def items_price_sidebar_gold(request): 
    url = SETTINGS_API_PRICE_GOLD_URL
    items_price_sidebar_gold = []
    try: 
        response = requests.get(url)
        if (response.status_code == HTTP_STATUS_SUCCESS): 
            items_price_sidebar_gold = response.json()[:SETTINGS_ITEM_PRICE_GOLD]
    except: 
        print("GET_GOLD: ERROR!")
    # with open('gold.json', 'w', encoding='utf-8') as f:
    #     json.dump(items_price_sidebar_gold, f, ensure_ascii=False)
    # print(items_price_sidebar_gold)
    return {
        "items_price_sidebar_gold": items_price_sidebar_gold
    }
