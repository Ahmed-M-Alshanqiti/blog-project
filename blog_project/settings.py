"""
Django settings for blog_project project.
"""
import os
from pathlib import Path
from datetime import timedelta
import dj_database_url
from dotenv import load_dotenv

# Load environment variables from .env file (if it exists)
load_dotenv() 

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# ----------------------------------------------------------------------
# Core Settings
# ----------------------------------------------------------------------

# Read from environment variables, providing secure defaults
SECRET_KEY = os.getenv("SECRET_KEY", "unsafe-secret-for-dev")
DEBUG = os.getenv("DEBUG", "False") == "True"
hosts = os.getenv("ALLOWED_HOSTS", "localhost,127.0.0.1")
ALLOWED_HOSTS = [h.strip() for h in hosts.split(",")] if hosts != "*" else ["*"]

# Application definition
INSTALLED_APPS = [
    # Django Core
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    "daphne",
    'django.contrib.staticfiles',
    
    # ASGI
    "channels",
    

    # Third-Party
    'rest_framework',
    'corsheaders',
    'rest_framework_simplejwt',
    "rest_framework_simplejwt.token_blacklist",
    'django_extensions', 

    # Local Apps
    'users',
    'posts',
    'comments',
    'blog',
    'api',
    "Chat",
    "notifications",
]

MIDDLEWARE = [
    # Security and HTTP Headers
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware", 
    "corsheaders.middleware.CorsMiddleware",

    # Core Django
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'blog_project.urls'
WSGI_APPLICATION = 'blog_project.wsgi.application'

# ----------------------------------------------------------------------
# Templates
# ----------------------------------------------------------------------

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'], 
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

# ----------------------------------------------------------------------
# Database
# ----------------------------------------------------------------------


# DATABASE_URL = os.getenv("DATABASE_URL")

# if DATABASE_URL:
#     DATABASES = {
#         "default": dj_database_url.parse(DATABASE_URL, conn_max_age=600)
#     }
# else:
DATABASES = {
        "default": {
            "ENGINE": os.getenv("DATABASE_ENGINE", "django.db.backends.postgresql"),
            "NAME": os.getenv("POSTGRES_DB", "postgres"),
            "USER": os.getenv("POSTGRES_USER", "postgres"),
            "PASSWORD": os.getenv("POSTGRES_PASSWORD", "postgres"),
            # 'localhost' for local development, 'db' for containerized web/asgi services
            "HOST": os.getenv("DATABASE_HOST", "localhost"),
            "PORT": os.getenv("DATABASE_PORT", 5432),
        }
    }

# ----------------------------------------------------------------------
# Cache (Redis)
# ----------------------------------------------------------------------

CACHE_TTL = 60 * 5 
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = os.getenv("REDIS_PORT", "6379")

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"redis://{REDIS_HOST}:{REDIS_PORT}/0", 
        "OPTIONS": {
            "CLIENT_CLASS": "redis.client.StrictRedis",
        }
    }
}

# ----------------------------------------------------------------------
# ASGI / Channels (Redis)
# ----------------------------------------------------------------------

ASGI_APPLICATION = "blog_project.asgi.application"

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [f"redis://{REDIS_HOST}:{REDIS_PORT}"], 
        },
    },
}

# ----------------------------------------------------------------------
# DRF / JWT / CORS Settings
# ----------------------------------------------------------------------

CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]
CORS_ALLOW_CREDENTIALS = True

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': ( 
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=55), 
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7), 
    'ROTATE_REFRESH_TOKENS': True, 
    'BLACKLIST_AFTER_ROTATION': True, 
}

# ----------------------------------------------------------------------
# Auth and Validation
# ----------------------------------------------------------------------

AUTH_USER_MODEL = "users.User"

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ----------------------------------------------------------------------
# Internationalization
# ----------------------------------------------------------------------

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ----------------------------------------------------------------------
# Static and Media Files
# ----------------------------------------------------------------------



STATIC_ROOT = os.getenv("STATIC_ROOT", BASE_DIR / "staticfiles")
MEDIA_ROOT =  BASE_DIR / "media"

LOGOUT_REDIRECT_URL = "/"

# Serving URLs
STATIC_URL = "/static/"
MEDIA_URL = "/media/"

# ----------------------------------------------------------------------
# Default Configuration
# ----------------------------------------------------------------------

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'