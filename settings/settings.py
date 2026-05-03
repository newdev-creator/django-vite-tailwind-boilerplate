from pathlib import Path

import environ

env = environ.Env()
environ.Env.read_env()
BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = env(
    "secret_key",
    default="django-insecure--w9czx&1-le5q^@)!-!o@$!znm=h2=x9y0nd*rcbmmbdf=w(q9",
)
DEBUG = env("DEBUG", default="False")

ALLOWED_HOSTS = env.list("ALLOWED_HOST", default=["*"])
CSRF_TRUSTED_ORIGINS = env.list("CSRF_TRUSTED_ORIGINS", default=["http://127.0.0.1"])

SITE_ID = 1

# ============================== Emails ============================== #
RESEND_API_KEY = env("RESEND_API_KEY", default=None)
EMAIL_TRANSACTION_SUBDOMAIN = "your_email_subdomain.com"
# ============================== Emails ============================== #

# ============================== Stripe ============================== #
STRIPE_PUBLIC_KEY = env("stripe_public_key", default=None)
STRIPE_SECRET_KEY = env("stripe_secret_key", default=None)
STRIPE_WEBHOOK_SECRET = env("stripe_webhook_secret", default=None)
# ============================== Stripe ============================== #

# ============================== Google ============================== #
GCP_CLIENT_ID = env("gcp_client_id", default=None)
GCP_SECRET = env("gcp_secret", default=None)
# ============================== Google ============================== #

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.sites",
    "django.contrib.sitemaps",
    "django.contrib.staticfiles",
    "apps.accounts.apps.AccountsConfig",
    "django_vite",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "django_cotton",
    "imagekit",
    "lucide",
]

if DEBUG:
    # Add django_browser_reload only in DEBUG mode
    INSTALLED_APPS += ["django_browser_reload"]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "allauth.account.middleware.AccountMiddleware",
]

if DEBUG:
    MIDDLEWARE += [
        "django_browser_reload.middleware.BrowserReloadMiddleware",
    ]

ROOT_URLCONF = "settings.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "settings.wsgi.application"


# Database
# https://docs.djangoproject.com/en/6.0/ref/settings/#databases

DATABASES = {
    "default": env.db("DATABASE_URL", default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}")
}


# Password validation
# https://docs.djangoproject.com/en/6.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/6.0/topics/i18n/

LANGUAGE_CODE = "fr-fr"

TIME_ZONE = "Europe/Paris"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/6.0/howto/static-files/

STATIC_URL = "static/"
STATICFILES_DIRS = [
    BASE_DIR / "static",
    BASE_DIR / "dist",
]
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

AUTH_USER_MODEL = "accounts.CustomUser"

STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

DJANGO_VITE = {
    "default": {
        "dev_mode": DEBUG,
        "manifest_path": BASE_DIR / "static" / ".vite" / "manifest.json",
    }
}

# ================================
# 📚 Logging
# ================================
# Create logs directory if it doesn't exist
LOGS_DIR = BASE_DIR / "logs"
LOGS_DIR.mkdir(parents=True, exist_ok=True)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "[{asctime}] {levelname} {name} {module}:{lineno} - {message}",
            "style": "{",
        },
    },
    "handlers": {
        "daily_file": {
            "level": "INFO",
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": LOGS_DIR / "app.log",
            "when": "midnight",  # rotation quotidienne
            "backupCount": 90,  # conservation 90 jours
            "encoding": "utf-8",
            "formatter": "verbose",
        },
        # (optionnel) affichage console pendant le dev
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "loggers": {
        # Logger principal de votre appli
        "": {  # '' = racine → tout le projet
            "handlers": ["daily_file", "console"],
            "level": "INFO",
            "propagate": False,  # évite les doublons
        },
        # Logger spécifique pour Django si besoin
        "django": {
            "handlers": ["daily_file"],
            "level": "INFO",
            "propagate": False,
        },
    },
}
