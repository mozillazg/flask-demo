#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os


SQLALCHEMY_DATABASE_URI = 'sqlite:///%s' % os.path.join(
    os.getcwd(), 'db.sqlite'
)
