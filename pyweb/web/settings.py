import os
from pathlib import Path

# Ruta base del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent

# Seguridad
SECRET_KEY = 'tu_clave_secreta_aqui'  # Cambia esto a una clave secreta única y mantenla en secreto
DEBUG = True  # Cambia a False en producción
ALLOWED_HOSTS = ['localhost', '127.0.0.1']  # Añade los dominios permitidos

# Aplicaciones instaladas
INSTALLED_APPS = [
    'django.contrib.admin',  # Administración de Django
    'django.contrib.auth',  # Autenticación
    'django.contrib.contenttypes',  # Tipos de contenido
    'django.contrib.sessions',  # Gestión de sesiones
    'django.contrib.messages',  # Mensajes
    'django.contrib.staticfiles',  # Archivos estáticos
    'myapp',  # Tu aplicación
]

# Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Configuración de las URLs
ROOT_URLCONF = 'myproject.urls'

# Plantillas
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'myapp/templates')],  # Carpeta de plantillas
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

# WSGI
WSGI_APPLICATION = 'myproject.wsgi.application'

# Base de datos
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',  # Usar SQLite como base de datos
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),  # Archivo de base de datos
    }
}

# Autenticación
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

# Internacionalización
LANGUAGE_CODE = 'es-es'  # Código de idioma
TIME_ZONE = 'UTC'  # Zona horaria
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Archivos estáticos
STATIC_URL = '/static/'  # URL para acceder a archivos estáticos
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'myapp/static'),  # Directorio de archivos estáticos
]

# Archivos multimedia
MEDIA_URL = '/media/'  # URL para acceder a archivos multimedia
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')  # Ruta del directorio de archivos multimedia

# Configuración de seguridad
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Configuración del logging (opcional)
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
        },
    },
}
