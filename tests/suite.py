#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

import pytest

from demo.apps.account.models import User


class BaseSuite(object):
    @pytest.fixture(autouse=True)
    def init(self, client):
        self.suite = client
        self.client = client.client
        self.app = client.app

    def prepare_account(self):
        with self.app.test_request_context():
            foo = User(username='foo', password='foo')

            bar = User(username='bar', password='bar')

            baz = User(username='baz', password='baz')
            self.suite.db.session.add(foo)
            self.suite.db.session.add(bar)
            self.suite.db.session.add(baz)
            self.suite.db.session.commit()

    def prepare_login(self, username='foo', password='foo'):
        self.prepare_account()
        rv = self.client.post('/accounts/login/', data={
            'username': username,
            'password': password
        }, follow_redirects=True)
        assert 'login success' in rv.data
