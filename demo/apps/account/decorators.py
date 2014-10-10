#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from functools import wraps

from flask import g, flash, request, redirect, url_for


def login_required(func):
    @wraps(func)
    def _wrapper(*args, **kwargs):
        if not g.user:
            flash('require login')
            return redirect(url_for('account.login', next=request.path))
        else:
            return func(*args, **kwargs)
    return _wrapper
