#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import (Blueprint, flash, render_template, abort, redirect,
                   request, url_for, session)
from .models import User

account = Blueprint('account', __name__,
                    url_prefix='/accounts',
                    template_folder='templates')


@account.route('/register/', methods=['GET', 'POST'])
def register():
    message = None
    if request.method == 'POST':
        username = request.form.get('username', '').lower()
        password = request.form.get('password', '').lower()

        if not all([username, password]):
            message = 'all input is required'
        elif User.query.filter_by(username=username).first():
            message = 'username %s has been registered' % username
        else:
            User.create_user(username, password)
            message = 'register success'
            flash(message)
            return redirect(url_for('.login'))

    flash(message)
    return render_template('register.html')


@account.route('/login/', methods=['GET', 'POST'])
def login():
    message = None
    if request.method == 'POST':
        username = request.form.get('username', '').lower()
        password = request.form.get('password', '').lower()

        if not all([username, password]):
            message = 'all input is required'
        else:
            user = User.login(username, password)
            if user:
                message = 'login success'
                session['user_id'] = user.get_id()
            else:
                message = 'username or password error'
            flash(message)
            return redirect(url_for('.index'))

    flash(message)
    return render_template('login.html')


@account.route('/')
def index():
    user_id = session.get('user_id')
    if not user_id:
        abort(403)
    else:
        return 'login as %s' % User.query.filter_by(id=user_id).first().username
