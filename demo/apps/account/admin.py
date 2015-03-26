#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from flask.ext.admin.contrib.sqla import ModelView

from demo.extensions import db


class UserAdmin(ModelView):
    def __init__(self, Model, **kwargs):
        super(UserAdmin, self).__init__(Model, db.session, **kwargs)
