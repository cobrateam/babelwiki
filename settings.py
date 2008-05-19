DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
     ('Andrews Medina', 'andrewsmedina@gmail.com'),
)

MANAGERS = ADMINS

TIME_ZONE = 'America/Sao_Paulo'

LANGUAGE_CODE = 'pt-br'

SITE_ID = 1

USE_I18N = True

MEDIA_ROOT = ''

MEDIA_URL = ''

ADMIN_MEDIA_PREFIX = '/media/'

SECRET_KEY = '#l4rl@d!+2p719of*&ew$374d%n!sb(cojkv%(94#!vz87expc'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
)

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
    'templates'
)

INSTALLED_APPS = (
    'wiki',
)
