APP_PATH_PAGE = "pages/"

APP_VALUE_LAYOUT_DEFAULT = "list"
APP_VALUE_STATUS_DEFAULT = "draft"
APP_VALUE_STATUS_ACTIVE = "published"
APP_VALUE_LAYOUT_CHOICE = (
    ('list', 'List'), 
    ('grid', 'Grid')
)
APP_VALUE_STATUS_CHOICE = (
    ('draft', 'Draft'),
    ('published', 'Published')
)
APP_VALUE_IMG_DEFAULT = "/media/news/images/no-image.png"

SETTINGS_ITEM_ARTICLE_SPECIAL = 5
SETTINGS_ITEM_ARTICLE_RANDOM = 3
SETTINGS_FEED_TITLE_PAGE_MESSAGE = "Tin tức tổng hợp "
SETTINGS_ARTICLE_NUMBER_PER_PAGE = 8
SETTINGS_ITEMS_ARTICLE_RELATED = 6
SETTINGS_ITEMS_ARTICLE_RECENT = 6
SETTINGS_ITEM_PRICE_COIN = 5
SETTINGS_ITEM_PRICE_GOLD = 5
SETTINGS_API_PRICE_COIN_URL = "http://apiforlearning.zendvn.com/api/get-coin"
SETTINGS_API_PRICE_GOLD_URL = "http://apiforlearning.zendvn.com/api/get-gold"
SETTINGS_FEED_TOTAL_ITEMS_SIDEBAR = 5
SETTINGS_CATEGORY_TOTAL_ITEMS_SIDEBAR = 5

TABLE_CATEGORY_SHOW = "Category"
TABLE_ARTICLE_SHOW = "Article"
TABLE_FEED_SHOW = "Feed"
TABLE_QUESTION_SHOW = "Question"
TABLE_CHOICE_SHOW = "Choice"

ADMIN_SRC_JS_FILES = ('my_admin/js/general.js',
            'my_admin/js/jquery-3.6.0.min.js',
            'my_admin/js/slugify.min.js')
ADMIN_SRC_CSS_FILES = {'all': ('my_admin/css/custom.css',)}

HTTP_STATUS_SUCCESS = 200
ADMIN_HEADER_NAME = "Linh Chi Admin"
