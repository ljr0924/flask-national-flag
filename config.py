"""
需要与media同一层目录
"""

import os

class Config():
    FLASK_APP = 'app.py'
    FLASK_SERVER = '127.0.0.1:5015'
    DEBUG = True
    MEDIA_ROOT = os.path.join(os.path.dirname(__file__), 'media')