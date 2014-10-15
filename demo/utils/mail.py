#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from flask import current_app
from flask.ext.mail import Message


def _send_mail(msg):
    app = current_app
    mail = app.extensions['mail']
    if not (msg.sender, mail.default_sender):
        return
    return mail.send(msg)


def send_mail(recipients, subject, message, **kwargs):
    msg = Message(recipients=recipients, subject=subject,
                  body=message, **kwargs)
    return _send_mail(msg)
