# -*- coding = utf-8 -*-
# @Time    : 2023/10/24 11:35
# @Author  : ShiChunWei
from .base import *  # NOQA

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
