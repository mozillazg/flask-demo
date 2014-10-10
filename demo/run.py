#!/usr/bin/env python
# -*- coding: utf-8 -*-
# import sys

# sys.path.insert(0, '../')

from flask import Flask
from database import db


def create_app(config=None):
    app = Flask(
        __name__,
        template_folder='templates',
    )
    app.config.from_pyfile('config.py')
    if isinstance(config, dict):
        app.config.update(config)
    app.static_folder = app.config.get('STATIC_FOLDER')

    db.init_app(app)
    db.app = app


    from demo.apps.account.views import account
    app.register_blueprint(account)
    from demo.apps.blog.views import blog
    app.register_blueprint(blog)

    return app


def create_db():
    from apps.account.models import User
    from apps.blog.models import Post, Comment
    db.create_all()

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
