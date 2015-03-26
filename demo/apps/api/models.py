#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

# import base64
from hashlib import sha1, sha256
import random
import time

from flask import current_app
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer,
                          BadSignature, SignatureExpired,
                          URLSafeSerializer)

from demo.extensions import db


class Client(db.Model):
    __tablename__ = 'api_client'

    id = db.Column(db.Integer, primary_key=True)
    api_key = db.Column(db.String, unique=True,
                        default=lambda: Client.generate_api_key())
    secret_key = db.Column(db.String, unique=True,
                           default=lambda: Client.generate_secret_key())

    app_name = db.Column(db.String, unique=True)
    # home_url = db.Column(db.URL)
    # description = db.Column(db.Text)
    # callback_url = db.Column(db.URL)

    # contact_person = db.Column(db.String)
    # contact_email = db.Column(db.Email)

    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(),
                           onupdate=db.func.now())

    def __repr__(self):
        return '<Client %r>' % (self.app_name)

    @staticmethod
    def __generate_key(string):
        app = current_app._get_current_object()
        s = URLSafeSerializer(app.config['SECRET_KEY'])
        string = '%s.%s.%s' % (string, time.time(), random.getrandbits(256))
        string = sha256(string).hexdigest()
        string = s.dumps(string)
        # return base64.b64encode(sha1(string).hexdigest(),
        #                         ).rstrip('==')
        return sha1(string).hexdigest()

    @classmethod
    def generate_api_key(cls):
        return cls.__generate_key('api_key')

    @staticmethod
    def generate_secret_key():
        return Client.__generate_key('secret_key')

    def generate_auth_token(self, expiration=None):
        app = current_app._get_current_object()
        s = Serializer(app.config['SECRET_KEY'],
                       expires_in=(expiration
                                   or app.config.get('API_TOKEN_EXPIRES', 3600)
                                   )
                       )
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        app = current_app._get_current_object()
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None    # valid token, but expired
        except BadSignature:
            return None    # invalid token
        else:
            return data
