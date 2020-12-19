from .settings_common import *

ALLOWED_HOSTS = []
DEBUG = True


# Logging 設定
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,

    # set logger
    'loggers':{
        # jdango logger
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
        },
        # menta app logger
        'menta':{
            'handlers':['console'],
            'level': 'DEBUG',
        },
    },
    # set handlers
    'handlers':{
        'console':{
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'dev'
        },
    },
    # set formatters
    'formatters': {
        'dev': {
            'format': 'format=%(asctime)s %(levelname)-8s %(message)s'
        },
    },
}
"""
  'formatters':{
        'dev': {
            'format':'//'.join([
                '%(asctime)s',
                '[%[(levelname)s]',
                '%(pathname)s(Line:%(loineno)d)',
                '%(messaeg)s'
            ])
        },
    }
"""


# メールの配信先をコンソールにする設定
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"


# メディアファイル：Webアプリを通じてアップロードされた静的ファイル（Webアプリを通さず最初から配置するファイルとは区別）
## メディアファイルの配置場所：MEDIA_ROOT
## 「https://<ホスト名>/media/hoge.jpg
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
