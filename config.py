# -*- coding: utf-8 -*-

import os

class Config():
    DEBUG = os.environ.get('SK_DEBUG') or True
    BASE_HOST = os.environ.get('SK_HOST') or 'localhost'
    BASE_PORT = os.environ.get('SK_PORT') or '3306'
    BASE_BASE = os.environ.get('SK_BASE') or 'sk_testd'
    BASE_USER = os.environ.get('SK_USER') or 'sk_testd'
    BASE_PASSWORD = os.environ.get('SK_PASSWORD') or 'skpassword'
    SK_TABLE = os.environ.get('SK_TABLE') or 'sk_table'
    SK_URL = os.environ.get('SK_URL') or 'http://analytics.skillfactory.ru:5000/api/v1.0/get_structure_course/'
    URL_TIMEOUT = os.environ.get('SK_URL_TIMEOUT') or 7

