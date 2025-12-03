"""
Django settings for setup project.
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-6$c45$1+7!hs$a(sqw3(m12h%e^jlzy3_=()yx$@o7kn#7sf3p"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Permite qualquer host (necessário para o Codespace)
ALLOWED_HOSTS = ['*']

# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    'colaboradores',
    "core",
    "equipamentos",
    "emprestimos",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "setup.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, 'templates')],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "setup.wsgi.application"

# Database - SQLite
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Password validation
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
LANGUAGE_CODE = "pt-br"
TIME_ZONE = "America/Sao_Paulo"
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = "static/"
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# Media Files (Upload de imagens)
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# --- CONFIGURAÇÕES DE SEGURANÇA DO CODESPACE (CRUCIAL PARA CORRIGIR O ERRO 403) ---

# 1. Confiar nas origens do GitHub Codespaces e Localhost
CSRF_TRUSTED_ORIGINS = [
    'https://*.github.dev',
    'https://*.app.github.dev',
    'https://*.gitpod.io',
    'http://127.0.0.1:8000',
    'http://localhost:8000',
    'https://localhost:8000'
]

# 2. Configurações de Cookie (DESATIVAR O 'SECURE' PARA EVITAR O ERRO)
# Se estiver True, o navegador pode bloquear o cookie se achar que a conexão não é HTTPS pura.
# Em produção real (servidor pago), isso deve ser True. No Codespace, False é mais seguro contra erros.
CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SECURE = False

# 3. Headers de Proxy
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Configurações de Login
LOGIN_URL = 'login' 
LOGIN_REDIRECT_URL = 'index' 
LOGOUT_REDIRECT_URL = 'home'