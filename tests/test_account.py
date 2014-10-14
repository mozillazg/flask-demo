#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from .suite import BaseSuite


class TestLogin(BaseSuite):
    def test_login_required(self):
        rv = self.client.get('/accounts/')
        assert 'login' in rv.location
        assert 'next' in rv.location

    def test_get(self):
        rv = self.client.get('/accounts/login/')
        assert '<form' in rv.data

    def test_invalid_account(self):
        rv = self.client.post(
            '/accounts/login/',
            data={'username': 'foo', 'password': 'bar'},
            follow_redirects=True
        )
        assert 'username or password error' in rv.data

    def test_password_error(self):
        rv = self.client.post(
            '/accounts/login/',
            data={'username': 'foo', 'password': 'barrr'},
            follow_redirects=True
        )
        assert 'username or password error' in rv.data

    def test_login_success(self):
        self.prepare_account()
        rv = self.client.post(
            '/accounts/login/',
            data={'username': 'foo', 'password': 'foo'},
        )
        assert rv.location.endswith('/accounts/')

    def test_index(self):
        self.prepare_login()
        rv = self.client.get('/accounts/')
        assert rv.status_code == 200
        assert 'foo' in rv.data

    def test_logout(self):
        self.prepare_login()
        rv = self.client.get('/accounts/logout/', follow_redirects=True)
        assert '<form' in rv.data
