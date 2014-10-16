#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask.ext.script import Manager, Server
from flask.ext.migrate import MigrateCommand

from demo.app import create_app

manager = Manager(create_app)
manager.add_option('-c', '--config', dest='config', required=False)
manager.add_command('runserver', Server())
manager.add_command('db', MigrateCommand)


@manager.command
def createdb():
    """Create database"""
    from demo.app import create_db
    create_db()

if __name__ == '__main__':
    manager.run()
