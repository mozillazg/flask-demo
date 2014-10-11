#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from pypinyin import slug as pinyin_slug
from demo.extensions import db


class Post(db.Model):
    __tablename__ = 'blog_post'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    content = db.Column(db.String)
    slug = db.Column(db.String(200), unique=True)

    user_id = db.Column(db.Integer, db.ForeignKey('account_user.id'))

    comments = db.relationship('Comment', backref='blog',
                               lazy='dynamic')

    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(),
                           onupdate=db.func.now())

    def __init__(self, title, content, user_id, slug=None):
        self.title = title
        self.content = content
        self.user_id = user_id
        self.slug = slug or pinyin_slug(self.title.replace(' ', ''))

    def __repr__(self):
        return '<Post %r>' % (self.title)


class Comment(db.Model):
    __tablename__ = 'blog_comment'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(100))

    user_id = db.Column(db.Integer, db.ForeignKey('account_user.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('blog_post.id'))

    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(),
                           onupdate=db.func.now())

    def __repr__(self):
        return '<Comment %r>' % (self.content[:20])

    def __init__(self, post_id, user_id, content):
        self.post_id = post_id
        self.user_id = user_id
        self.content = content
