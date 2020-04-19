AUTHOR = 'and-semakin'
SITENAME = 'Питонические атаки'
SITESUBTITLE = 'Про разработку в целом и в частности про Python'
SHOW_SOCIAL_ON_INDEX_PAGE_HEADER = True
SITEURL = ''

PATH = 'content'
ARTICLE_PATHS = ['blog']
ARTICLE_SAVE_AS = '{date:%Y}/{slug}/index.html'
ARTICLE_URL = '{date:%Y}/{slug}/'

PAGE_PATHS = ['pages']
PAGE_SAVE_AS = 'pages/{slug}/index.html'
PAGE_URL = 'pages/{slug}/'
DISPLAY_PAGES_ON_MENU = True

STATIC_PATHS = ['static', 'pages']

DEFAULT_METADATA = {
    'status': 'draft',
}

TIMEZONE = 'Asia/Yekaterinburg'

DEFAULT_LANG = 'ru'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (('Pelican', 'http://getpelican.com/'),
         ('Python.org', 'http://python.org/'),)

# Social widget
SOCIAL = (('github', 'https://github.com/and-semakin'),
          ('telegram', 'https://t.me/bro0ke'),
          ('linkedin', 'https://www.linkedin.com/in/%D0%B0%D0%BD%D0%B4%D1%80%D0%B5%D0%B9-%D1%81%D0%B5%D0%BC%D0%B0%D0%BA%D0%B8%D0%BD-501619108/'),)

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True

THEME = 'themes/pelican-clean-blog'
COLOR_SCHEME_CSS = 'monokai.css'
