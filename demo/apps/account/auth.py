#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from flask.ext.login import current_user,  login_user, logout_user
# from demo.extensions import login_manager
from .models import User


# @login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()
#
#
# @login_manager.request_loader
# def load_user_from_request(request):
#
#     # first, try to login using the api_key url arg
#     api_key = request.args.get('api_key')
#     if api_key:
#         user = User.query.filter_by(api_key=api_key).first()
#         if user:
#             return user
#
#     # next, try to login using Basic Auth
#     api_key = request.headers.get('Authorization')
#     if api_key:
#         api_key = api_key.replace('Basic ', '', 1)
#         try:
#             api_key = base64.b64decode(api_key)
#         except TypeError:
#             pass
#         user = User.query.filter_by(api_key=api_key).first()
#         if user:
#             return user
#
#     # finally, return None if both methods did not login the user
#     return None
