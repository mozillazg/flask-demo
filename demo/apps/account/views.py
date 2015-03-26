#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import (Blueprint, flash, render_template, redirect,
                   request, url_for, session, g)
from .auth import current_user, login_user, logout_user
from .decorators import login_required
from .models import User

account = Blueprint('account', __name__,
                    url_prefix='/accounts',
                    template_folder='templates')


@account.before_request
def before_request():
    if current_user.is_authenticated():
        g.user = current_user
    else:
        g.user = None


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
    if message:
        flash(message)
    return render_template('account/register.html')


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
                login_user(user)
            else:
                message = 'username or password error'
            flash(message)
            next_url = request.args.get('next', url_for('.index'))
            return redirect(next_url)
    if message:
        flash(message)
    return render_template('account/login.html')


@account.route('/')
@login_required
def index():
    user_id = session.get('user_id')
    return render_template('account/index.html',
                           user=User.query.filter_by(id=user_id))


@account.route('/logout/')
def logout():
    logout_user()
    flash('logout success')
    return redirect(url_for('.login'))
