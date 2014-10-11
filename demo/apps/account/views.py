#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import (Blueprint, flash, render_template, redirect,
                   request, url_for, session, g)
from .decorators import login_required
from .forms import SubmitForm
from .models import User

account = Blueprint('account', __name__,
                    url_prefix='/accounts',
                    template_folder='templates')


@account.before_request
def before_request():
    g.user = None
    if 'user_id' in session:
        g.user = User.query.get(session['user_id'])


@account.route('/register/', methods=['GET', 'POST'])
def register():
    message = None
    form = SubmitForm()
    if form.validate_on_submit():
        username = form.username.data.strip()
        password = form.password.data.strip()

        User.create_user(username, password)
        message = 'register success'
        flash(message)
        return redirect(url_for('.login'))
    if message:
        flash(message)
    return render_template('account/register.html', form=form)


@account.route('/login/', methods=['GET', 'POST'])
def login():
    message = None
    form = SubmitForm()
    if form.validate_on_submit():
        username = form.username.data.strip()
        password = form.password.data.strip()

        user = User.login(username, password)
        if user:
            message = 'login success'
            session['user_id'] = user.get_id()
        else:
            message = 'username or password error'
        flash(message)
        next_url = request.args.get('next', url_for('.index'))
        return redirect(next_url)
    if message:
        flash(message)
    return render_template('account/login.html', form=form)


@account.route('/')
@login_required
def index():
    user_id = session.get('user_id')
    return render_template('account/index.html',
                           user=User.query.filter_by(id=user_id))


@account.route('/logout/')
def logout():
    del session['user_id']
    flash('logout success')
    return redirect(url_for('.login'))
