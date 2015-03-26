#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from functools import wraps

from flask import request, Blueprint
from flask.ext.restful import abort, Api, Resource, reqparse

from .models import Client

bp = Blueprint('api', __name__)
api = Api(bp, catch_all_404s=True)


def token_required(func):
    @wraps(func)
    def _wrapper(*args, **kwargs):
        token = request.values.get('token') or request.authorization.username
        if not (token and Client.verify_auth_token(token)):
            return abort(403, message='token is invalid or expired')
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

    def get(self):
        return self.post()

    def post(self):
        args = self.reqparse.parse_args()
        client_id = args['client_id']
        client_secret = args['client_secret']
        client = Client.query.filter_by(api_key=client_id,
                                        secret_key=client_secret).first()
        if not client:
            abort(403, message='client_id and/or client_secret is invalid')
        else:
            return {
                'token': client.generate_auth_token(3600),
                'expires_in': 3600,
            }

api.add_resource(TokenAPI, '/token')
