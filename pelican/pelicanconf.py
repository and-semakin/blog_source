import functools

import plural_ru


AUTHOR = "Андрей Семакин"
SITENAME = "Питонические атаки"
SITESUBTITLE = "Про разработку в целом и про Python в частности"
SHOW_SOCIAL_ON_INDEX_PAGE_HEADER = True
SITEURL = ""
SLUGIFY_SOURCE = "basename"
DEFAULT_DATE_FORMAT = ("ru_RU", '%d %B %Y, %a')

PATH = "content"
ARTICLE_PATHS = ["blog"]
ARTICLE_SAVE_AS = "{date:%Y}/{date:%m}/{slug}/index.html"
ARTICLE_URL = "{date:%Y}/{date:%m}/{slug}/"

PAGE_PATHS = ["pages"]
PAGE_SAVE_AS = "pages/{slug}/index.html"
PAGE_URL = "pages/{slug}/"
DISPLAY_PAGES_ON_MENU = True

STATIC_PATHS = ["static", "extra", "pages"]
EXTRA_PATH_METADATA = {
    "extra/favicon_16.png": {"path": "favicon_16.png"},
    "extra/favicon_24.png": {"path": "favicon_24.png"},
    "extra/favicon_32.png": {"path": "favicon_32.png"},
    "extra/CNAME": {"path": "CNAME"},
    "extra/.nojekyll": {"path": ".nojekyll"},
    "extra/README.md": {"path": "README.md"},
    "extra/robots.txt": {"path": "robots.txt"},
}

DEFAULT_CATEGORY = "blog"
DISPLAY_CATEGORIES_ON_MENU = False
DEFAULT_METADATA = {
    "status": "draft",
}

TIMEZONE = "Asia/Yekaterinburg"

DEFAULT_LANG = "ru"

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Social widget
SOCIAL = (("rss", "/feeds/all.atom.xml"), ("telegram", "https://t.me/pythonic_attacks"))

# Menu items
MENUITEMS = [("Тэги", "/tags.html")]

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True

THEME = "themes/pelican-clean-blog"
COLOR_SCHEME_CSS = "monokai.css"

UTTERANCES_REPO = "and-semakin/and-semakin.github.io"

PLUGIN_PATHS = ["plugins"]
PLUGINS = ["sitemap", "filetime_from_git", "post_stats"]
# disabled plugins:
# * deadlinks

SITEMAP = {
    "format": "xml",
    "priorities": {"articles": 0.5, "indexes": 0.5, "pages": 0.5},
    "changefreqs": {"articles": "monthly", "indexes": "daily", "pages": "monthly"},
}
# DEADLINK_VALIDATION = False
# DEADLINK_OPTS = {
#     "archive": True,
#     "classes": [],
#     "labels": False,
#     "timeout_duration_ms": 10000,
#     "timeout_is_error": True,
# }

GIT_FILETIME_FROM_GIT = True

SHOW_READ_TIME = True
PLURAL_MINUTE = functools.partial(
    plural_ru.ru, quantitative=["минута", "минуты", "минут"]
)

DISABLE_CUSTOM_THEME_JAVASCRIPT = False


def sort_by_number_of_articles(tags):
    return sorted(tags, reverse=True, key=lambda tag: len(tag[1]))


# Custom filters
JINJA_FILTERS = {'sort_by_number_of_articles': sort_by_number_of_articles}

# Custom Markdown config.
# See MARKDOWN here:
# https://docs.getpelican.com/en/stable/settings.html#basic-settings
MARKDOWN = {
    'extension_configs': {
        'markdown.extensions.codehilite': {'css_class': 'highlight'},
        'markdown.extensions.meta': {},
        'pymdownx.extra': {},
    },
    'output_format': 'html5',
}
