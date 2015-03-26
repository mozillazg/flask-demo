#!/usr/bin/env python
# -*- coding: utf-8 -*-
# import sys
import os

# sys.path.insert(0, '../')

from flask import Flask
from flask.ext.mail import Mail
from flask.ext.migrate import Migrate
from extensions import admin, cache, db, login_manager


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
    cache.init_app(app)
    register_admins(app)
    Mail(app)
    migrate = Migrate()
    migrate.init_app(app, db)

    register_login(app)

    from demo.apps.account.views import account
    from demo.apps.blog.views import blog
    app.register_blueprint(account)
    app.register_blueprint(blog)

    return app


def register_admins(app):
    from demo.apps.account.models import User
    from demo.apps.blog.models import Post
    from demo.apps.blog.models import Comment
    from demo.apps.account.admin import UserAdmin
    from demo.apps.blog.admin import PostAdmin, CommentAdmin

    admin.add_view(UserAdmin(User))
    admin.add_view(PostAdmin(Post))
    admin.add_view(CommentAdmin(Comment))
    admin.init_app(app)


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
