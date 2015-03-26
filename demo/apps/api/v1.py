#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from flask import Blueprint
from flask.ext.restful import abort, Api, reqparse, Resource

from demo.apps.todo.models import Task
from demo.extensions import db
from . import token_required

API_VERSION_V1 = 1
API_VERSION = API_VERSION_V1
bp = Blueprint('api_v1', __name__)
api_v1 = Api(bp, catch_all_404s=True)


class TaskListAPI(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title', type=str, required=True,
                                   help='title is required', location='json')
        self.reqparse.add_argument('description', type=str,
                                   default='', location='json')
        super(TaskListAPI, self).__init__()

    @token_required
    def get(self):
        tasks = Task.query.all()
        data = [{'id': t.id, 'title': t.title, 'description': t.description}
                for t in tasks]
        return data

    @token_required
    def post(self):
        args = self.reqparse.parse_args()
        task = Task()
        task.title = args['title']
        task.description = args['description']
        db.session.add(task)
        db.session.commit()

        data = {
            'id': task.id,
            'title': task.title,
            'description': task.description,
        }
        return data, 201


class TaskAPI(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title', type=str, required=True,
                                   help='title is required', location='json')
        self.reqparse.add_argument('description', type=str,
                                   default='', location='json')
        super(TaskAPI, self).__init__()

    @token_required
    def get(self, id):
        task = Task.query.filter_by(id=id).first()
        if not task:
            abort(404, message="Task %s doesn't exist" % id)

        data = {
            'id': task.id,
            'title': task.title,
            'description': task.description,
        }
        return data

    @token_required
    def put(self, id):
        task = Task.query.filter_by(id=id).first()
        if not task:
            abort(404, message="Task %s doesn't exist" % id)
        args = self.reqparse.parse_args()
        task.title = args['title']
        task.description = args['description']
        db.session.add(task)
        db.session.commit()

        data = {
            'id': task.id,
            'title': task.title,
            'description': task.description,
        }
        return data

    @token_required
    def delete(self, id):
        task = Task.query.filter_by(id=id).first()
        if not task:
            abort(404, message="Task %s doesn't exist" % id)
        db.session.delete(task)
        db.session.commit()

        # return {}


api_v1.add_resource(TaskListAPI, '/tasks')
api_v1.add_resource(TaskAPI, '/tasks/<int:id>')
