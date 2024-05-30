from django.utils import timezone
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from re import escape
from django.urls import reverse
from .apiview.api_view_helpers import ListCreateAPIViewBase, RetrieveUpdateDestroyAPIViewBase
from .forms import CheckoutForm, ContactForm
from .serializers import *
from .models import *
from .define import *
from .helpers import *
from .send_mail import mail_content_contact, mail_content_order, send_mail
from rest_framework.permissions import (
    IsAuthenticated,
    AllowAny,
    IsAuthenticatedOrReadOnly,
    IsAdminUser,
)

# Create your views here.


def index(request):
    # by default, it will goes to index of news app
    # WHY? In DJango, when we render, it will run all templates folder
    # without differentiating, it will just go to the first
    # /templates/ folder in the folder structure

    items_blog = Blog.objects.filter(
        status=APP_VALUE_STATUS_ACTIVE,
        publish_date__lte=timezone.now()).order_by('-publish_date')

    items_category = Category.objects.filter(
        status=APP_VALUE_STATUS_ACTIVE,
        is_homepage=True).order_by("ordering")

    for category in items_category:
        category.product_filter = category.product_set.filter(
            status=APP_VALUE_STATUS_ACTIVE,
            special=True
        ).order_by("-id")  # add the product by the newest item

    items_latest_product = chunked(
        Product.objects.filter(
            status=APP_VALUE_STATUS_ACTIVE).order_by("-id")[:SETTINGS_PRODUCT_LATEST_TOTAL],
        SETTINGS_PRODUCT_PER_COL)

    items_hot_product = chunked(
        Product.objects.filter(
            status=APP_VALUE_STATUS_ACTIVE).order_by("-total_sold")[:SETTINGS_PRODUCT_HOT_TOTAL],
        SETTINGS_PRODUCT_PER_COL)

    items_random_product = chunked(
        Product.objects.filter(
            status=APP_VALUE_STATUS_ACTIVE).order_by("?")[:SETTINGS_PRODUCT_RANDOM_TOTAL],
        SETTINGS_PRODUCT_PER_COL)

    return render(request, APP_PATH_SHOP_PAGE + "index.html", {
        "title_page": "Homepage",
        "items_category": items_category,
        "items_latest_product": items_latest_product,
        "items_hot_product": items_hot_product,
        "items_random_product": items_random_product,
        "items_blog": items_blog
    })


def product(request, product_slug, product_id):
    item_product = get_object_or_404(
        Product,
        slug=product_slug,
        id=product_id,
        status=APP_VALUE_STATUS_ACTIVE)

    items_product_related = Product.objects.filter(
        category=item_product.category,
        status=APP_VALUE_STATUS_ACTIVE).order_by("-id").exclude(id=product_id)[:SETTINGS_PRODUCT_RELATED_TOTAL]

    return render(request, APP_PATH_SHOP_PAGE + "detail.html", {
        "title_page": item_product.name,
        "item_product": item_product,
        "items_product_related": items_product_related
    })


def category(request, category_slug="shop"):
    item_category = None
    items_product = []
    planting_methods = PlantingMethod.objects.filter(
        status=APP_VALUE_STATUS_ACTIVE).order_by("ordering")[:SETTINGS_PLANTING_METHOD_TOTAL]
    items_category = Category.objects.filter(
        status=APP_VALUE_STATUS_ACTIVE).order_by("ordering")[:SETTINGS_CATEGORIES_TOTAL]
    items_latest_product = chunked(
        Product.objects.filter(
            status=APP_VALUE_STATUS_ACTIVE).order_by("-id")[:SETTINGS_PRODUCT_LATEST_TOTAL_SIDEBAR],
        SETTINGS_PRODUCT_PER_COL)

    if category_slug != "shop":
        item_category = get_object_or_404(
            Category,
            slug=category_slug,
            status=APP_VALUE_STATUS_ACTIVE)
        items_product = Product.objects.filter(
            category=item_category,
            status=APP_VALUE_STATUS_ACTIVE).order_by("-id")
    else:
        items_product = Product.objects.filter(
            status=APP_VALUE_STATUS_ACTIVE).order_by("-id")

    params = {
        # must be "price" or "-price"
        "order": request.GET.get("order") if request.GET.get("order") == "price" else "-price",
        "minPrice": request.GET.get("minPrice", ""),
        "maxPrice": request.GET.get("maxPrice", ""),
        "planting": request.GET.get("planting", ""),
        "keyword": request.GET.get("keyword", "")
    }
    items_product = items_product.order_by(params["order"]+"_real")

    if params["minPrice"]:
        items_product = items_product.filter(
            price_real__gte=params["minPrice"])

    if params["maxPrice"]:
        items_product = items_product.filter(
            price_real__lte=params["maxPrice"])

    if params["planting"]:
        # planting methods having id same as params[planting]
        items_product = items_product.filter(
            planting_methods__id=params["planting"])

    if params["keyword"]:
        items_product = items_product.filter(
            # regular expression, iregex = in-case-sensitive regular regex
            name__iregex=escape(params["keyword"])
        ).order_by("-id")

    # count before paginator
    products_count = items_product.all().count()

    paginator = Paginator(
        items_product, per_page=SETTINGS_PRODUCT_NUMBER_PER_PAGE)
    items_product = paginator.get_page(request.GET.get("page"))

    return render(request, APP_PATH_SHOP_PAGE + "category.html", {
        "title_page": item_category.name if item_category else "Shop",
        "item_category": item_category,
        "items_category": items_category,
        "items_product": items_product,
        "items_latest_product": items_latest_product,
        "planting_methods": planting_methods,
        "products_count": products_count,
        "paginator": paginator,
        "params": params,
    })

# when the user click on add to cart, we have to save the item and its quantity in SESSION
# Session is where the workers work


def cart(request):
    items_product_cart = []
    total_price = 0
    # When we close the browser, everything in the session is deleted
    if "cart" in request.session:
        cart = request.session.get("cart")
        for product_id, quantity in cart.items():
            product = Product.objects.get(id=product_id)
            item_price = product.price_real*quantity
            total_price += item_price
            items_product_cart.append({
                "id": product_id,
                "product": product,
                "item_price": item_price,
                "quantity": quantity
            })

    return render(request, APP_PATH_SHOP_PAGE + "cart.html", {
        "title_page": "Cart",
        "total_price": total_price,
        "items_product_cart": items_product_cart
    })


def checkout(request):
    cart = request.session.get("cart", {})
    form = CheckoutForm()
    if not cart:
        absolute_url = request.build_absolute_uri(reverse("shop:cart"))
        return redirect(absolute_url)

    if request.method == "POST":
        form = CheckoutForm(request.POST)  # validate
        if form.is_valid():
            return checkout_post(request, form, cart)

    items_product_checkout = []
    total_order = 0
    for product_id, quantity in cart.items():
        product = Product.objects.get(id=product_id)
        total = product.price_real*quantity
        total_order += total
        items_product_checkout.append({
            "name": product.name,
            "total": total,
            "quantity": quantity
        })
    return render(request, APP_PATH_SHOP_PAGE + "checkout.html", {
        "title_page": "Checkout Order",
        "items_product_checkout": items_product_checkout,
        "total_order": total_order,
        "form": form
    })


def checkout_post(request, form, cart):
    name = form.cleaned_data["name"]
    email = form.cleaned_data["email"]
    phone = form.cleaned_data["phone"]
    address = form.cleaned_data["address"]
    code = generate_order_code(length=SETTINGS_GENERATE_CODE_ORDER_LENGTH)
    # save ORDER and ORDER_ITEM
    order = Order.objects.create(
        code=code,
        name=name,
        email=email,
        phone=phone,
        address=address
    )
    total_order = 0
    quantity_order = 0
    items_order_mail = []
    for product_id, quantity in cart.items():
        product = Product.objects.get(id=product_id)
        price = product.price_real
        total = price*quantity
        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=quantity,
            price=price,
            total=total
        )
        total_order += total
        quantity_order += quantity
        items_order_mail.append({
            "product": product.name,
            "quantity": quantity,
            "price": price,
            "total": total
        })
    order.total = total_order
    order.quantity = quantity_order
    order.save()
    del request.session['cart']

    link_order_check = request.build_absolute_uri(reverse("shop:check_order"))

    mail_content = mail_content_order(
        order_code=code,
        name=name,
        email=email,
        phone=phone,
        address=address,
        total_order=total_order,
        items_order_mail=items_order_mail,
        link_order_check=link_order_check
    )
    send_mail(
        NOTIFY_EMAIL_SUBJECT_SUCCESS_ORDER,
        content=mail_content,
        email_to=[email],
        email_bcc=[ADMIN_EMAIL_RECEIVE]
    )
    absolute_url = request.build_absolute_uri(
        reverse("shop:success")) + '?t=order'
    return redirect(absolute_url)


def success(request):
    notify = NOTIFY_ORDER_SUCCESS
    t = request.GET.get('t')
    if t == "contact":
        notify = NOTIFY_CONTACT_SUCCESS
    return render(request, APP_PATH_SHOP_PAGE + "success.html", {
        "title_page": "Notification",
        "notify": notify
    })


def contact(request):
    form = ContactForm()
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            return contact_post(request, form)

    return render(request, APP_PATH_SHOP_PAGE + "contact.html", {
        "title_page": "Contact",
        "form": form,
    })


def contact_post(request, form):
    name = form.cleaned_data["name"]
    email = form.cleaned_data["email"]
    phone = form.cleaned_data["phone"]
    message = form.cleaned_data["message"]

    contacted = False
    Contact.objects.create(
        name=name,
        email=email,
        phone=phone,
        message=message,
        contacted=contacted
    )

    # SEND MAIL FOR CONTACT
    mail_content = mail_content_contact(name, email, phone, message)
    send_mail(
        NOTIFY_EMAIL_SUBJECT_SUCCESS_CONTACT,
        content=mail_content,
        email_to=[email],
        email_bcc=[ADMIN_EMAIL_RECEIVE]
    )

    absolute_url = request.build_absolute_uri(
        reverse("shop:success")) + '?t=contact'
    return redirect(absolute_url)


def add_to_cart(request):
    if request.method == "POST":
        product_id = request.POST.get("id")
        product_quantity = request.POST.get("quantity")
        cart = request.session.get("cart", {})
        # client already add same product beforehand, so accumulate
        if product_id in cart:
            cart[product_id] += int(product_quantity)
        else:
            cart[product_id] = int(product_quantity)

        request.session["cart"] = cart
        # signalling the session change, so session is saved again
        request.session.modified = True

    absolute_url = request.build_absolute_uri(reverse("shop:cart"))
    return redirect(absolute_url)


def update_cart(request):
    product_id = str(request.GET.get("productId"))
    action = request.GET.get("action")
    cart = request.session.get("cart", {})
    print("HELLO I GET CART", cart)
    if product_id in cart:
        if action == "decrease":
            if cart[product_id] > 1:
                cart[product_id] -= 1
            else:
                del cart[product_id]
        elif action == "increase":
            cart[product_id] += 1
        elif action == "delete":
            del cart[product_id]

    request.session["cart"] = cart
    absolute_url = request.build_absolute_uri(reverse("shop:cart"))

    return redirect(absolute_url)


def check_order(request):
    if request.method == "POST":
        return check_order_post(request)

    return render(request, APP_PATH_SHOP_PAGE + "check-order.html", {
        "title_page": "Check order",
    })


def check_order_post(request):
    order_code = request.POST.get('code', '').strip()  # same as trim in JS
    error_message = ""
    item_order = None

    if order_code == "":
        error_message = NOTIFY_ORDER_CODE_EMPTY_MESSAGE
    else:
        try:
            item_order = Order.objects.get(code=order_code)
        except Order.DoesNotExist:  # exception for order cannot be found
            error_message = NOTIFY_ORDER_CODE_NOT_FOUND_MESSAGE

    return render(request, APP_PATH_SHOP_PAGE + "check-order.html", {
        "title_page": "Check order",
        "order_code": order_code,
        "error_message": error_message,
        "item_order": item_order
    })


def blog(request, blog_slug, blog_id):
    item_blog = get_object_or_404(
        Blog,
        slug=blog_slug,
        status=APP_VALUE_STATUS_ACTIVE,
        publish_date__lte=timezone.now()
    )

    items_blog_related = chunked(
        Blog.objects.filter(
            status=APP_VALUE_STATUS_ACTIVE,
            publish_date__lte=timezone.now()).order_by('-publish_date').exclude(slug=item_blog.slug)[:SETTINGS_ITEMS_BLOG_RELATED],
        SETTINGS_PRODUCT_PER_COL)

    items_blog = chunked(Blog.objects.all(), SETTINGS_PRODUCT_PER_COL)

    return render(request, APP_PATH_SHOP_PAGE + "blog.html", {
        "title_page": "Homepage",
        "item_blog": item_blog,
        "items_blog_related": items_blog_related,
        "items_blog": items_blog[:3]
    })

# ---------------------------- API DOCUMENTATIONS -------------------------------


class ShopCategoryListCreateAPIView(ListCreateAPIViewBase):
    serializer_class = ShopCategorySerializer
    model_class = Category
    permission_classes = [IsAuthenticated]


class ShopCategoryRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIViewBase):
    serializer_class = ShopCategorySerializer
    model_class = Category
    permission_classes = [IsAuthenticated]


class ShopProductListCreateAPIView(ListCreateAPIViewBase):
    serializer_class = ShopProductSerializer
    model_class = Product
    permission_classes = [IsAuthenticated]


class ShopProductRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIViewBase):
    serializer_class = ShopProductSerializer
    model_class = Product
    permission_classes = [IsAuthenticated]


class ShopBlogListCreateAPIView(ListCreateAPIViewBase):
    serializer_class = ShopBlogSerializer
    model_class = Blog
    permission_classes = [IsAuthenticated]


class ShopBlogRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIViewBase):
    serializer_class = ShopBlogSerializer
    model_class = Blog
    permission_classes = [IsAuthenticated]


class ShopPlantingMethodListCreateAPIView(ListCreateAPIViewBase):
    serializer_class = PlantingMethodSerializer
    model_class = PlantingMethod
    permission_classes = [IsAuthenticated]


class ShopPlantingMethodRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIViewBase):
    serializer_class = PlantingMethodSerializer
    model_class = PlantingMethod
    permission_classes = [IsAuthenticated]
