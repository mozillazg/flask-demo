#!/usr/bin/env python
# -*- coding: utf-8 -*-
# import sys
import os

# sys.path.insert(0, '../')

from flask import Flask
from extensions import db


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

    from demo.apps.account.views import account
    app.register_blueprint(account)
    from demo.apps.blog.views import blog
    app.register_blueprint(blog)
    from demo.apps.api.v1 import bp, API_VERSION
    app.register_blueprint(bp, url_prefix='%s/v%s' % ('/api', API_VERSION))

    return app


def create_db():
    db.create_all()


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0')
