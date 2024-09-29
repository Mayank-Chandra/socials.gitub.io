from .base import *
from decouple import config

DEBUG=False

ADMINS=[
    ('Mayank Chandra','socialthrouglens@gmail.com')
]

ALLOWED_HOSTS=['socialsthroughlens.com','www.socialsthroughlens.com']

DATABASES = {
'default': {
'ENGINE': 'django.db.backends.postgresql',
'NAME': config('POSTGRES_DB'),
'USER': config('POSTGRES_USER'),
'PASSWORD': config('POSTGRES_PASSWORD'),
'HOST': 'db',
'PORT': 5432,
}
}
CSRF_COOKIE_SECURE=True
SESSION_COOKIE_SECURE=True
SECURE_SSL_REDIRECT=True