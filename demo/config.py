#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os


SECRET_KEY = 'your secret key'

SQLALCHEMY_DATABASE_URI = 'sqlite:///%s' % os.path.join(
    os.getcwd(), 'db.sqlite'
)
