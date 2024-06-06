from .base import *



DEBUG = True



DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "perfume",
        "USER": 'perfume_admin',
        "PASSWORD":os.getenv('POSTGRES_PASSWORD'),
        "HOST": "localhost",
        "PORT": 5432,
    }
}