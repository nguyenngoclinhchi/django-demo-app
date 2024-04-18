APP_PATH_PAGE = "pages/"
APP_PATH_SHOP_PAGE = "shop/pages/"

APP_VALUE_LAYOUT_DEFAULT = "list"
APP_VALUE_STATUS_DEFAULT = "draft"
APP_VALUE_STATUS_ACTIVE = "published"
APP_VALUE_ORDER_STATUS_DEFAULT = "order"
APP_VALUE_ORDER_STATUS_CONFIRM = "confirm"
APP_VALUE_ORDER_STATUS_DELIVERY = "delivery"
APP_VALUE_ORDER_STATUS_FINISH = "finish"

APP_VALUE_LAYOUT_CHOICE = (
    ('list', 'List'), 
    ('grid', 'Grid')
)
APP_VALUE_STATUS_CHOICE = (
    ('draft', 'Draft'),
    ('published', 'Published')
)
APP_VALUE_ORDER_STATUS_CHOICE = (
    ('order', 'Order'),
    ('confirm', 'Confirm'),
    ('delivery', 'Delivery'),
    ('finish', 'Finish')
)

APP_VALUE_IMG_DEFAULT = "/media/shop/images/no-image.png"

SETTINGS_PRODUCT_LATEST_TOTAL = 9
SETTINGS_PRODUCT_HOT_TOTAL = 9
SETTINGS_PRODUCT_RANDOM_TOTAL = 9
SETTINGS_PRODUCT_RELATED_TOTAL = 6

SETTINGS_PRODUCT_PER_COL = 3
SETTINGS_PRODUCT_NUMBER_PER_PAGE = 9

SETTINGS_CATEGORIES_TOTAL = 6
SETTINGS_PLANTING_METHOD_TOTAL = 4

SETTINGS_PRODUCT_LATEST_TOTAL_SIDEBAR = 9
SETTINGS_GENERATE_CODE_ORDER_LENGTH = 10

SETTINGS_CATEGORIES_TOTAL_MENU = 6

SETTINGS_ITEMS_BLOG_RELATED = 9

TABLE_CATEGORY_SHOW = "Category"
TABLE_CONTACT_SHOW = "Contact"
TABLE_PLANTING_METHOD = "Planting method"
TABLE_PRODUCT_SHOW = "Product"
TABLE_ORDER_SHOW = "Order"
TABLE_ORDER_ITEM_SHOW = "Order Item"
TABLE_BLOG_SHOW = "Blog"

NOTIFY_ORDER_SUCCESS = "Thank you for placing order with us"
NOTIFY_CONTACT_SUCCESS = "Thank you for contacting us"

NOTIFY_ORDER_CODE_EMPTY_MESSAGE = "Please enter the order code"
NOTIFY_ORDER_CODE_NOT_FOUND_MESSAGE = "Cannot find the order, please check the order code again"

NOTIFY_EMAIL_SUBJECT_SUCCESS_CONTACT = "LinhChi - Notification for successful contact"
NOTIFY_EMAIL_SUBJECT_SUCCESS_ORDER = "LinhChi - Notification for successful order"

ADMIN_EMAIL_RECEIVE = "nguyenngoclinhchi@u.nus.edu"
ADMIN_HEADER_NAME = "Linh Chi Admin"

ADMIN_SRC_JS_FILES = (
    'my_admin/js/general.js',
    'my_admin/js/jquery-3.6.0.min.js',
    'my_admin/js/slugify.min.js')

ADMIN_SRC_CSS_FILES = {'all': ('my_admin/css/custom.css',)}
HTTP_STATUS_SUCCESS = 200
