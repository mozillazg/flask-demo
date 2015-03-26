#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from flask.ext.admin.contrib.sqla import ModelView

from demo.extensions import db


class PostAdmin(ModelView):
    def __init__(self, Model, **kwargs):
        super(PostAdmin, self).__init__(Model, db.session, **kwargs)


class CommentAdmin(ModelView):
    def __init__(self, Model, **kwargs):
        super(CommentAdmin, self).__init__(Model, db.session, **kwargs)
