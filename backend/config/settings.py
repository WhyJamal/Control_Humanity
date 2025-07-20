import environ, os
from pathlib import Path
from datetime import timedelta
from celery.schedules import crontab

BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))
SECRET_KEY = env('SECRET_KEY')

DEBUG = env.bool('DEBUG')

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=[])

INSTALLED_APPS = [
    'jazzmin',
    'import_export',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'django_celery_beat',
    
    'tasks.apps.TasksConfig',
    'accounts',
    'projects',
    'chat',
    'ratings',
    # "django_rq",
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'
ASGI_APPLICATION = 'config.asgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / env('DB_NAME', default='db.sqlite3'),
        'OPTIONS': {
            'timeout': 20,
        },
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'ru'
TIME_ZONE = 'Asia/Tashkent'
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    BASE_DIR / "config/static",
]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'accounts.User'

CORS_ALLOWED_ORIGINS = env.list('CORS_ALLOWED_ORIGINS', default=[])

CSRF_TRUSTED_ORIGINS = CORS_ALLOWED_ORIGINS

user_rate = env.int('DEFAULT_THROTTLE_RATES_USER', 100)
anon_rate = env.int('DEFAULT_THROTTLE_RATES_ANON', 10)

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.UserRateThrottle',
        'rest_framework.throttling.AnonRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'user': f'{user_rate}/minute',
        'anon': f'{anon_rate}/minute',
    },
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(
        minutes=env.int('ACCESS_TOKEN_LIFETIME_MINUTES')
    ),
    'REFRESH_TOKEN_LIFETIME': timedelta(
        days=env.int('REFRESH_TOKEN_LIFETIME_DAYS')
    ),
}

CORS_ALLOW_ALL_ORIGINS = True

TELEGRAM_BOT_TOKEN = env('TELEGRAM_BOT_TOKEN')

CELERY_BROKER_URL = env('CELERY_BROKER_URL')
CELERY_RESULT_BACKEND = env('CELERY_RESULT_BACKEND')
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'

CELERY_BEAT_SCHEDULE = {
    'mark-overdue-tasks-daily': {
        'task': 'tasks.tasks.mark_overdue_tasks',
        'schedule': crontab(minute='*/1'), #'schedule': crontab(hour=0, minute=0),  # har kuni soat 00:00 da ishga tushadi
    },
}

CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers.DatabaseScheduler'


JAZZMIN_SETTINGS = {
    "site_title": "AP soft",
    "site_header": "All personal soft",
    "site_brand": "All personal soft",
    "site_logo": "images/CompanyLogo.png",
    "login_logo": "images/CompanyLogo.png",
    "welcome_sign": "Добро пожаловать.",
    "copyright": "All personal soft",
    
    "order_with_respect_to": [
        "accounts", 
        "projects",
        "tasks",
        "chat",
        "ratings"
    ],
    
    "icons": {
        # Accounts app
        "accounts.User": "fas fa-user",
        "auth.Group": "fas fa-users",
        
        # Projects app
        "projects.Project": "fas fa-project-diagram",
        
        # Tasks app
        "tasks.Task": "fas fa-tasks",
        "tasks.Status": "fas fa-list-ol",
        
        # Chat app
        "chat.ChatRoom": "fas fa-comments",
        "chat.Message": "fas fa-comment",
        
        # Ratings app
        "ratings.Rating": "fas fa-star",
    },
    
    "related_modal_active": True,
    "custom_css": "css/admin-custom.css",
    "custom_js": "js/admin-custom.js",
    "show_ui_builder": True,
}