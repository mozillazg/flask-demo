#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.cache import Cache

cache = Cache()
db = SQLAlchemy()
