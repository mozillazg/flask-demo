#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from demo.database import db


class User(db.Model):
    __tablename__ = 'account_user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, unique=True, nullable=False)

    posts = db.relationship('Post', backref='author', lazy='dynamic')
    comments = db.relationship('Comment', backref='author', lazy='dynamic')

    def __init__(self, username='', password=''):
        self.username = username
        self.password = password

    def get_id(self):
        return unicode(self.id)

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True

    @classmethod
    def create_user(cls, username, password):
        user = cls(username.lower(), password.lower())
        db.session.add(user)
        db.session.commit()
        return user

    @classmethod
    def login(cls, username, password):
        user = cls.query.filter_by(username=username, password=password
                                   ).first()
        if user:
            return user

    def __str__(self):
        return self.username

    def __repr__(self):
        return '<User: %r>' % self.username
