#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask.ext.admin import Admin
from flask.ext.cache import Cache
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager

admin = Admin(name='Flask Demo')
cache = Cache()
db = SQLAlchemy()
login_manager = LoginManager()
