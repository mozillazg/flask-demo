#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import tempfile

import pytest

from demo.app import create_app
from demo.extensions import db


class Client(object):
    def __init__(self):
        config = {'TESTING': True,
                  'WTF_CSRF_ENABLED': False,
                  'WTF_CSRF_CHECK_DEFAULT': False,
                  'SECRET_KEY': 'secret-key-for-test',
                  }
        self.db_fd, self.db_file = tempfile.mkstemp()
        config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///%s' % self.db_file

        self.app = create_app(config)
        self.client = self.app.test_client()
        db.create_all()
        self.db = db

    def clean(self):
        self.db.session.remove()
        self.db.drop_all()
        os.close(self.db_fd)
        os.unlink(self.db_file)


@pytest.fixture(scope='function')
def client(request):
    client = Client()
    request.addfinalizer(client.clean)
    return client
