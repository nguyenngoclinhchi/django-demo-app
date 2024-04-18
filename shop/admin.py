from django.contrib import admin
from django.http import HttpRequest
from django.utils.html import format_html

from .helpers import get_currency_vn
from .models import *
from .define import *

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    class Media: 
        js = ADMIN_SRC_JS_FILES
        css = ADMIN_SRC_CSS_FILES

    list_display = (
        'id',
        'name', 
        'status', 
        'is_homepage', 
        'ordering'
    )
    # prepopulated_fields = {'slug': ('name' ,)}
    list_filter = ('status', 'is_homepage')
    search_fields = ['name']

class PlantingMethodAdmin(admin.ModelAdmin):
    class Media: 
        js = ADMIN_SRC_JS_FILES
        css = ADMIN_SRC_CSS_FILES

    list_display = (
        'name', 
        'slug', 
        'is_homepage', 
        'status', 
        'ordering'
    )
    list_filter = ('status', 'is_homepage')
    search_fields = ['name']
    # prepopulated_fields = {'slug': ('name',)}  # Automatically populate the slug field based on the name field

class ProductAdmin(admin.ModelAdmin):
    class Media:
        js = ADMIN_SRC_JS_FILES
        css = ADMIN_SRC_CSS_FILES

    # in new Django version there is no ordering inside list_display
    list_display = (
        'name', 
        'display_image',
        'get_planting_methods', 
        'status', 
        'ordering', 
        'category', 
        'special', 
        'get_price_formatted', 
        'get_price_sale_formatted', 
        'get_price_real_formatted', 
        'total_sold',
        'image'
    )
    list_editable = ['image']
    empty_value_display = "-not on sale-"

    # prepopulated_fields = {'slug': ('name' ,)}
    list_filter = ('status', 'special', 'category', 'planting_methods')
    search_fields = ['name', 'category__name', 'planting_methods__name']

    # obj is each item in the table
    @admin.display(description="Planting Methods")
    def get_planting_methods (self, obj): 
        methods = [method.name for method in obj.planting_methods.all()]
        return ', '.join(methods)

    @admin.display(description="Price")
    def get_price_formatted (self, obj): 
        return get_currency_vn(obj.price)

    @admin.display(description="Price Sale")
    def get_price_sale_formatted (self, obj): 
        return get_currency_vn(obj.price_sale) if obj.price_sale else None

    @admin.display(description="Price Real")
    def get_price_real_formatted (self, obj): 
        return get_currency_vn(obj.price_real)

    @admin.display(description="Image")
    def display_image (self, obj): 
        # url = obj.image.url if obj.image else "news/images/feed/no_image.jpg"
        return format_html('<img src="{}" width="50" height="50" />', obj.image.url if obj.image else APP_VALUE_IMG_DEFAULT)

class ContactAdmin(admin.ModelAdmin):
    class Media: 
        js = ADMIN_SRC_JS_FILES
        css = ADMIN_SRC_CSS_FILES

    list_display = (
        'name', 
        'email', 
        'phone', 
        'contacted', 
        'created', 
        'message', 
        'message_admin'
    )
    list_filter = ['contacted', 'created']
    search_fields = ('name', 'email', 'phone', 'message')
    readonly_fields = ('name', 'email', 'phone', 'message', 'created')
    ordering = ['-created']
    list_editable = ['contacted']

    # usually, Django will put the editable field above and show others below
    # but, I want to show them in order instead
    fields = ['name', 'email', 'phone', 'contacted', 'created', 'message', 'message_admin']

    # only users outside can create the contact, the admin is not allowed
    def has_add_permission(self, request: HttpRequest) -> bool:
        # return super().has_add_permission(request)
        return False

class OrderAdmin(admin.ModelAdmin):
    class OrderItemAdminInline(admin.TabularInline):
        model = OrderItem
        class Media: 
            js = ADMIN_SRC_JS_FILES
            css = ADMIN_SRC_CSS_FILES

        readonly_fields = (
            'order', 
            'product', 
            'quantity',
            'price',
            'total',
            'price_formatted', 
            'total_formatted'
        )
        fields = (
            'order', 
            'product', 
            'quantity', 
            'price_formatted', 
            'total_formatted'
        )
        can_delete = False
        view_on_site = True
        # search_fields = ['order__name', 'product__name']
        # list_filter = ['order__status']
        # raw_id_fields = ['order', 'product']

        def has_add_permission(self, request, obj=None):
            return False

        @admin.display(description="Price")
        def price_formatted (self, obj): 
            return get_currency_vn(obj.price)

        @admin.display(description="Total")
        def total_formatted (self, obj): 
            return get_currency_vn(obj.total)

    class Media: 
        js = ADMIN_SRC_JS_FILES
        css = ADMIN_SRC_CSS_FILES

    readonly_fields = (
        'code', 
        'name', 
        'email', 
        'phone', 
        'created', 
        'quantity', 
        'total_formatted', 
        'address', 
        'total'
    )
    fields = [
        'status', 
        'code', 
        'name', 
        'email', 
        'phone', 
        'address', 
        'created', 
        ('quantity', 'total_formatted'),
    ]
    list_display = (
        'code', 
        'name', 
        'email', 
        'phone', 
        'created', 
        'quantity', 
        'total_formatted', 
        'status',
        'order_detail'
    )
    search_fields = ['name', 'code', 'email', 'phone']
    list_filter = ['status', 'name']
    ordering = ['-created']
    list_editable = ['status']
    inlines = [OrderItemAdminInline]

    def has_add_permission(self, request):
        return False

    @admin.display(description="Total")
    def total_formatted (self, obj): 
        return get_currency_vn(obj.total)

    # When user click save, this function is called
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if obj.status == APP_VALUE_ORDER_STATUS_FINISH:
            obj.update_total_sold()

    def order_detail(self, obj):
        order_items_display = ''
        for item in obj.orderitem_set.all():
            order_items_display += '{}:{}<br/>'.format(item.product.name, item.quantity)
        return format_html(order_items_display)

class BlogAdmin(admin.ModelAdmin):
    class Media: 
        js = ADMIN_SRC_JS_FILES
        css = ADMIN_SRC_CSS_FILES

    # in new Django version there is no ordering inside list_display
    list_display = (
        'name', 
        'display_image', 
        'image',
        'status', 
        'ordering', 
        'special')
    # prepopulated_fields = {'slug': ('name' ,)}
    list_filter = ('status','special')
    search_fields = ['name']
    list_editable = ['image']

    @admin.display(description="image")
    def display_image (self, obj): 
        return format_html('<img src="{}" width="50" height="50" />', obj.image.url if obj.image else APP_VALUE_IMG_DEFAULT)

# Register the PlantingMethod model with the custom admin interface
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(PlantingMethod, PlantingMethodAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Blog, BlogAdmin)

admin.site.site_header = ADMIN_HEADER_NAME
