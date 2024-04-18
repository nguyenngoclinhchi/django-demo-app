from django.contrib import admin
from .models import Article, Category, Feed
from .define import *
from django.utils.html import format_html

class CategoryAdmin(admin.ModelAdmin):
    # in new Django version there is no ordering inside list_display
    list_display = ('name', 'status', 'is_homepage', 'layout', 'ordering')
    # prepopulated_fields = {'slug': ('name' ,)}
    list_filter = ('layout', 'status', 'is_homepage')
    search_fields = ['name']
    class Media: 
        js = ADMIN_SRC_JS_FILES
        css = ADMIN_SRC_CSS_FILES

class ArticleAdmin(admin.ModelAdmin):
    # in new Django version there is no ordering inside list_display
    list_display = ('name', 'display_image', 'publish_date', 'category', 'status', 'ordering', 'special')
    # prepopulated_fields = {'slug': ('name' ,)}
    list_filter = ('status','special','category',)
    search_fields = ['name']
    class Media: 
        js = ADMIN_SRC_JS_FILES
        css = ADMIN_SRC_CSS_FILES

    @admin.display(description="image")
    def display_image (self, obj): 
        return format_html('<img src="{}" width="50" height="50" />', obj.image.url if obj.image else APP_VALUE_IMG_DEFAULT)

class FeedAdmin(admin.ModelAdmin):
    # in new Django version there is no ordering inside list_display
    list_display = ('name', 'status', 'ordering')
    # prepopulated_fields = {'slug': ('name' ,)}
    list_filter = ('status',)
    search_fields = ['name']
    class Media: 
        js = ADMIN_SRC_JS_FILES

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'pub_date', 'was_published_recently')
    list_filter = ('pub_date',)
    search_fields = ['question_text']

admin.site.register(Category, CategoryAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Feed, FeedAdmin)

admin.site.site_header = ADMIN_HEADER_NAME