#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

DEBUG = False
TESTING = False

# account
SECRET_KEY = 'your secret key'

# session
# SESSION_COOKIE_NAME = '_s'
# SESSION_COOKIE_SECURE = True
# PERMANENT_SESSION_LIFETIME = 3600 * 24 * 30

# Flask-SQLAlchemy
SQLALCHEMY_DATABASE_URI = 'sqlite:///%s' % os.path.join(
    os.getcwd(), 'db.sqlite'
)
# SQLALCHEMY_POOL_SIZE = 100
# SQLALCHEMY_POOL_TIMEOUT = 10
# SQLALCHEMY_POOL_RECYCLE = 3600

# Flask-Mail
# MAIL_SERVER = 'smtp.gmail.com'
# MAIL_USE_SSL = True
# MAIL_USERNAME = ''
# MAIL_PASSWORD = ''
# MAIL_DEFAULT_SENDER = ('name', 'noreply@email.com')
