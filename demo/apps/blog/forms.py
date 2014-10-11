#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from flask.ext.wtf import Form
from flask.ext.wtf.form import _Auto
from wtforms import TextField, TextAreaField
from wtforms.validators import Required, ValidationError

from .models import Post


class PostForm(Form):
    title = TextField('title', [Required()])
    slug = TextField('slug', [Required()])
    content = TextAreaField('content', [Required()])

    def __init__(self, formdata=_Auto, obj=None, *args, **kwargs):
        self._obj = obj
        super(PostForm, self).__init__(formdata=formdata, obj=obj, *args, **kwargs)

    def validate_slug(form, field):
        slug = field.data
        if form._obj:
            post_id = form._obj.id
            if Post.query.filter(Post.id != post_id, Post.slug == slug).first():
                raise ValidationError('slug exists')
        else:
            if Post.query.filter_by(slug=slug).first():
                raise ValidationError('slug exists')


class CommentForm(Form):
    content = TextAreaField('content', [Required()])
