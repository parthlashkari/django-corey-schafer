"""
Django settings for django_corey_schafer project.

Generated by 'django-admin startproject' using Django 3.0.8.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
import django_heroku

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))#this tells the location of our source code in the local computer.
# print(BASE_DIR)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

SECRET_KEY = os.environ.get('SECRET_KEY') #we write this os.environ.get(which is an environment variable) so that when we put this source code on github or public then nobody can see our secret key or use it.
DEBUG_VALUE = os.environ.get('DEBUG_VALUE')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False #we make debug false when site is in production and debug true when site is in development
# DEBUG = True


# i have to make this settings.py file usable both for production and development but as of now this settings.py file only supports production and for localhost:8000(or development) this will not work
ALLOWED_HOSTS = ['parthbookdjango.herokuapp.com', 'localhost:8000']
# ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',


    'blog.apps.BlogConfig',
    'users.apps.UsersConfig',
    'crispy_forms', #this is a third party package which will make the forms look good.

    'django_cleanup.apps.CleanupConfig', #this will take care of deleting old updates automatically when user updates his profile pic or post.

    'social_django', #this is used for social authentication like login from fb,google or twitter

    'whitenoise.runserver_nostatic',
    #'users',
    #'blog',
]

AUTHENTICATION_BACKENDS = [
    'social_core.backends.github.GithubOAuth2', 
    'social_core.backends.google.GoogleOAuth2',
    'social_core.backends.facebook.FacebookOAuth2',
    'django.contrib.auth.backends.ModelBackend', #we have to put this when using social authentication 
    'blog.authentication.EmailAuthbackend', #this is for sending confirmation email when users first time registers
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'social_django.middleware.SocialAuthExceptionMiddleware',
]

ROOT_URLCONF = 'django_corey_schafer.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,"templates")],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',


                'django.template.context_processors.media',
                'social_django.context_processors.backends',# this and below one are for social authentication via google or fb etc. 
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'django_corey_schafer.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'Parth',
#         'USER': 'postgres',
#         'PASSWORD':os.environ.get('POSTGRESQL_PASSWORD'),
#         'HOST': 'parthbookdjango.herokuapp.com',
#         'PORT': 5432
#     }
# }

#we have used this database because heroku server wants this database not conventional dbsqlite3.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DJANGO_DATABASE_NAME'),
        'USER': os.environ.get('DJANGO_DATABASE_USER'),
        'HOST': os.environ.get('DJANGO_DATABASE_HOST'),
        'PORT': 5432,
        'PASSWORD': os.environ.get('DJANGO_DATABASE_PASSWORD')
    }
}



import dj_database_url #for telling the heroku server that we r using the current database in the system in the heroku server.

db_from_env = dj_database_url.config(conn_max_age=600)
DATABASES['default'].update(db_from_env)
# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/
# STATIC_ROOT = os.path.join(BASE_DIR,"static") #when using static files in the localhost server we use this 
STATIC_ROOT = os.path.join(BASE_DIR,"staticfiles")# when using the static files in the heroku server we use this
# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, "staticfiles"),
# ]

STATIC_URL = '/static/' #for telling our website where to search for all the static files in the system

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage' #this will take care of storing al the static files in the heroku server and caching them temporarily

MEDIA_ROOT = os.path.join(BASE_DIR,"media") #for telling our localhost server that where are all the medial files like images and video.

MEDIA_URL = '/media/' #for telling our website where to search for all the media files in the system

CRISPY_TEMPLATE_PACK = 'bootstrap4' #for telling crispy forms that we wanna use bootstrap 4 

LOGIN_REDIRECT_URL = 'blog:blog-home' #after login successfully completed where to send the login user in this blog is the app_name mentioned in the blog.urls.py file and blog-home is the name of view that we want to use

LOGIN_URL = 'login-page' #that after typing https://xyz.com/login where to send the user and login-page is the name of view

# LOGOUT_REDIRECT_URL = 'logout-page'


SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = os.environ.get('SOCIAL_AUTH_GOOGLE_OAUTH2_KEY')  #these all keys and secrets are very essential to use the social authentication in the website and always keep them secret

SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = os.environ.get('SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET') 

SOCIAL_AUTH__KEY = os.environ.get('SOCIAL_AUTH__KEY') 

SOCIAL_AUTH_GITHUB_KEY = os.environ.get('SOCIAL_AUTH_GITHUB_KEY') 

SOCIAL_AUTH_GITHUB_SECRET = os.environ.get('SOCIAL_AUTH_GITHUB_SECRET')

SOCIAL_AUTH_FACEBOOK_KEY = os.environ.get('SOCIAL_AUTH_FACEBOOK_KEY')

SOCIAL_AUTH_FACEBOOK_SECRET = os.environ.get('SOCIAL_AUTH_FACEBOOK_SECRET')

EMAIL_BACKEND =  'django.core.mail.backends.smtp.EmailBackend' #for sending mails directly to users and if we console in place of smtp then we can see the mail only in command prompt

EMAIL_HOST = 'smtp.gmail.com'

EMAIL_PORT = 587

EMAIL_USE_TLS = True

EMAIL_HOST_USER = os.environ.get('EMAIL_USER')  #for sending mail this id will be used

EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_PASS') #and for sending mail this password will be used

AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID') #since for deploying our site on heroku we need this fle storage system by aws s3 becaue heroku doesn't provide any file storage system of its own , files means images and videos and docs files

AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')

AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME') #this is bucket we have created in aws s3  to use for file storing

AWS_S3_FILE_OVERWRITE = False #like when user choose to upload the file with the same name that akready exists in the aws s3 bucket then it will not overwrite it and rather make a new file

AWS_DEFAULT_ACL = None

AWS_S3_REGION_NAME = 'ap-south-1' #from where we are using aws s3 like in   our case it is mumbai asia pacific

AWS_S3_SIGNATURE_VERSION = 's3v4'  # version of aws s3

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage' 

# django_heroku.settings(locals())
django_heroku.settings(config=locals(), staticfiles=False,logging=False) #for using django-heroku this is needed

#this is for allowing multiple  logins at the same time
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': ('%(asctime)s [%(process)d] [%(levelname)s] '
                       'pathname=%(pathname)s lineno=%(lineno)s '
                       'funcname=%(funcName)s %(message)s'),
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        }
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    }
}
