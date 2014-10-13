#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from functools import wraps

from flask import request, Blueprint
from flask.ext.restful import abort, Api, Resource, reqparse

bp = Blueprint('api', __name__)
api = Api(bp, catch_all_404s=True)


def token_required(func):
    @wraps(func)
    def _wrapper(*args, **kwargs):
        token = request.args.get('token')
        if not token:
            return abort(401)
        return func(*args, **kwargs)
    return _wrapper


def token_required(func):
    @wraps(func)
    def _wrapper(*args, **kwargs):
        token = request.args.get('token')
        if not token:
            return abort(401)
        return func(*args, **kwargs)
    return _wrapper


class TokenAPI(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('client_id', type=str, required=True,
                                   help='client_id is required', location='json')
        self.reqparse.add_argument('client_secret', type=str, required=True,
                                   help='client_secret is required', location='json')
        super(TokenAPI, self).__init__()

    def post(self):
        args = self.reqparse.parse_args()
        return {
            'token': 'token',
            'expires_in': 3600,
        }

api.add_resource(TokenAPI, '/token')
