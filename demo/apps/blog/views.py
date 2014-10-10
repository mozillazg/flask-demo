#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import (Blueprint, flash, render_template, redirect,
                   request, url_for, session, g)
from demo.apps.account.decorators import login_required
from demo.apps.blog.models import Post, Comment
from demo.apps.account.models import User
from demo.database import db

blog = Blueprint('blog', __name__, url_prefix='/blog',
                 template_folder='templates')


@blog.before_request
def before_request():
    g.user = None
    if 'user_id' in session:
        g.user = User.query.get(session['user_id'])


@blog.route('/')
@login_required
def index():
    # data = Post.query.order_by(db.desc(Post.updated_at)).all()
    data = Post.query.order_by(db.desc(Post.created_at)).all()
    return render_template('blog/index.html', data=data)


@blog.route('/new/', methods=['GET', 'POST'])
def new():
    if request.method == 'POST':
        title = request.form['title']
        slug = request.form['slug']
        content = request.form['content']
        user_id = g.user.id
        post = Post(title, content, user_id, slug)
        db.session.add(post)
        db.session.commit()

        flash('add success')
        return redirect(url_for('.index'))
    return render_template('blog/add.html', data=None)


@blog.route('/delete/', methods=['POST'])
def delete():
    post = Post.query.get(request.form['post_id'])
    db.session.delete(post)
    db.session.commit()
    flash('delete success')
    return redirect(url_for('.index'))


@blog.route('/edit/<int:post_id>/<slug>/', methods=['GET', 'POST'])
def edit(post_id, slug):
    post = Post.query.get(post_id)
    if request.method == 'POST':
        post_id = request.form['post_id']
        title = request.form['title']
        slug = request.form['slug']
        content = request.form['content']
        user_id = g.user.id

        post.title = title
        post.slug = slug
        post.content = content
        post.user_id = user_id

        db.session.add(post)
        db.session.commit()

        flash('edit success')
        return redirect(url_for('.index'))
    return render_template('blog/add.html', data=post)


@blog.route('/view/<int:post_id>/<slug>/')
def view(post_id, slug):
    post = Post.query.get_or_404(post_id)
    comments = post.comments
    return render_template('blog/view.html', post=post, comments=comments)


@blog.route('/new_comment/<int:post_id>/', methods=['POST'])
@login_required
def new_comment(post_id):
    post = Post.query.get_or_404(post_id)
    comment = Comment(post_id=post.id,
                      user_id=g.user.id,
                      content=request.form['content']
                      )
    db.session.add(comment)
    db.session.commit()

    return redirect(request.form['next'])
