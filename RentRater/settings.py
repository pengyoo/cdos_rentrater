"""
Django settings for RentRater project.

Generated by 'django-admin startproject' using Django 5.0.3.

"""
from pathlib import Path
import boto3
import json


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production

# Get Secret Key from AWS Secrets Manager 
def get_secret(secret_name):
    client = boto3.client('secretsmanager', region_name='eu-west-1')
    response = client.get_secret_value(SecretId=secret_name)
    secret_string = response['SecretString']
    return secret_string

AWS_SECRET_NAME = 'x22196242/rentrater/prod'
secret_value = json.loads(get_secret(AWS_SECRET_NAME))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = secret_value['DJANGO_SECRET_KEY']
# SECRET_KEY = 'django-insecure-q+876v5ok5)-pt^r&^3@%1ep=z04o=-ng90xikczn1+@to+v*0'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['172.31.45.192', '34.241.53.5','d5d5f9065c6b477da340a081c1aaa450.vfs.cloud9.eu-west-1.amazonaws.com', 'x22196242-rentrater-env.eba-qwpzib2f.eu-west-1.elasticbeanstalk.com']
CSRF_TRUSTED_ORIGINS = ['https://d5d5f9065c6b477da340a081c1aaa450.vfs.cloud9.eu-west-1.amazonaws.com']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # add apps
    'rater',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'RentRater.urls'

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

WSGI_APPLICATION = 'RentRater.wsgi.application'


# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
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


# Internationalization
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'static'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Redirect to home page after sign in
LOGIN_REDIRECT_URL = '/'


# AWS s3
# S3_BUCKET = 'elasticbeanstalk-eu-west-1-845708981828'
S3_BUCKET = 'x22196242-rentrater-bucket'
S3_IMAGE_PATH = 'images/rentrater/'
