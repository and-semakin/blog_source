AUTHOR = 'and-semakin'
SITENAME = 'Питонические атаки'
SITESUBTITLE = 'Блог Андрея Семакина'
SHOW_SOCIAL_ON_INDEX_PAGE_HEADER = True
SITEURL = ''

PATH = 'content'

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
          ('twitter', 'https://twitter.com/and_semakin'),)

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True

THEME = 'themes/pelican-clean-blog'
COLOR_SCHEME_CSS = 'monokai.css'
