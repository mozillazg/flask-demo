#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.admin import Admin

db = SQLAlchemy()
admin = Admin(name='Flask Demo')
