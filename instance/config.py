import os
import urllib.parse


class Config:
    SECRET_KEY = os.urandom(24)
    DEBUG = True