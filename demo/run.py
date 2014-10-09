from flask import Flask

from database import dbs


def create_app(config=None):
    app = Flask(
        __name__,
        template_folder='templates',
    )
    app.config.from_pyfile('config.py')
    if isinstance(config, dict):
        app.config.update(config)
    app.static_folder = app.config.get('STATIC_FOLDER')

    for db in dbs:
        db.init_app(app)
        db.app = app

    return app


def create_db():
    for db in dbs:
        db.create_all()

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
