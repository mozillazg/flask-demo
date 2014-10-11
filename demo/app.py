#!/usr/bin/env python
# -*- coding: utf-8 -*-
# import sys
import os

# sys.path.insert(0, '../')

from flask import Flask
from extensions import db, login_manager


def create_app(config=None):
    app = Flask(
        __name__,
        template_folder='templates',
    )
    app.config.from_pyfile('config.py')
    if isinstance(config, dict):
        app.config.update(config)
    elif config:
        app.config.from_pyfile(os.path.realpath(config))
    app.static_folder = app.config.get('STATIC_FOLDER')

    db.init_app(app)
    db.app = app

    register_login(app)

    from demo.apps.account.views import account
    app.register_blueprint(account)
    from demo.apps.blog.views import blog
    app.register_blueprint(blog)

    return app


def register_login(app):
    login_manager.login_view = 'account.login'
    login_manager.init_app(app)
    from apps.account.auth import load_user
    login_manager.user_loader(load_user)
    # from apps.account.auth import load_user_from_request
    # login_manager.request_loader(load_user_from_request)


def create_db():
    db.create_all()


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0')
