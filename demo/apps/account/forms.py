#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from flask.ext.wtf import Form
from wtforms import TextField, PasswordField
from wtforms.validators import Required


class SubmitForm(Form):
    username = TextField('Username', [Required()])
    password = PasswordField('Password', [Required()])
