#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import (Blueprint, flash, render_template, redirect,
                   request, url_for, g)
from demo.apps.account.decorators import login_required
from demo.apps.blog.models import Post, Comment
from demo.apps.account.auth import current_user
from demo.extensions import cache, db
from demo.apps.blog.forms import PostForm, CommentForm

blog = Blueprint('blog', __name__, url_prefix='/blog',
                 template_folder='templates')


@cache.memoize(timeout=50)   # cache normal function
def func_foobar(a, b):
    import time
    return a + b + time.time()


@blog.before_request
def before_request():
    if current_user.is_authenticated():
        g.user = current_user
    else:
        g.user = None


@blog.route('/')
@login_required
@cache.cached(timeout=60 * 1, key_prefix='all_posts')  # cache view function
def index():
    # data = Post.query.order_by(db.desc(Post.updated_at)).all()
    data = Post.query.order_by(Post.created_at.desc()).all()
    return render_template('blog/index.html', data=data)


@blog.route('/new/', methods=['GET', 'POST'])
def new():
    form = PostForm()

    if form.validate_on_submit():
        title = form.title.data
        slug = form.title.data
        content = form.content.data

        user_id = g.user.id
        post = Post(title, content, user_id, slug)
        db.session.add(post)
        db.session.commit()

        flash('add success')
        return redirect(url_for('.index'))
    return render_template('blog/add.html', data=None, form=form)


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
    form = PostForm(request.form, post)

    if form.validate_on_submit():
        title = form.title.data
        slug = form.slug.data
        content = form.content.data
        user_id = g.user.id

        post.title = title
        post.slug = slug
        post.content = content
        post.user_id = user_id

        db.session.add(post)
        db.session.commit()

        flash('edit success')
        return redirect(url_for('.index'))
    return render_template('blog/add.html', data=post, form=form)


@blog.route('/view/<int:post_id>/<slug>/')
def view(post_id, slug):
    post = Post.query.get_or_404(post_id)
    comments = post.comments
    form = CommentForm()
    return render_template('blog/view.html', post=post, comments=comments,
                           form=form)


@blog.route('/new_comment/<int:post_id>/', methods=['POST'])
@login_required
def new_comment(post_id):
    post = Post.query.get_or_404(post_id)
    form = CommentForm(request.form)
    if form.validate_on_submit():
        comment = Comment(post_id=post.id,
                          user_id=g.user.id,
                          content=form.content.data
                          )
        db.session.add(comment)
        db.session.commit()

    return redirect(request.form['next'])
