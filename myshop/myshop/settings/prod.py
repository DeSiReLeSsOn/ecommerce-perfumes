import os
from .base import *



DEBUG = False



ADMINS = [
    ('Jonhy D', 'theproblemdi@gmail.com'),
]



ALLOWED_HOSTS = ['*']




DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "perfume",
        "USER": 'perfume_admin',
        "PASSWORD":os.getenv('POSTGRES_PASSWORD'),
        'HOST': 'postgres-db',
        "PORT": 5432,
    }
}