#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask
from flask import url_for
from flask import request
from flask import render_template
from flask import make_response
from flask import abort
from flask import redirect
from flask import session
from flask import escape
from werkzeug import secure_filename

app = Flask(__name__)


@app.route('/')
def index():
    return 'Index Page'


@app.route('/hello')
def hello_world():
    return 'Hello World!'


@app.route('/user/<username>')
def show_user_profile(username):
    return 'User %s' % username


@app.route('/post/<int:post_id>')
def show_post(post_id):
    return 'Post %d' % post_id


@app.route('/number/<float:number>')
def show_number(number):
    return 'Number %f' % number


@app.route('/url/<path:url>')
def show_url(url):
    return 'Url %s' % url


@app.route('/projects/')
def projects():
    return 'The project page'


@app.route('/urls/')
def urls():
    return '%s<br />%s' % (url_for('hello_world'),
                          url_for('show_number', number=1.3))


@app.route('/hello2/')
@app.route('/hello2/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # if valid_login(request.form['username'],
                       # request.form['password']):
            # return log_the_user_in(request.form['username'])
        # else:
            # error = 'Invalid username/password'
        return 'POST'
    else:
        return 'GET'


@app.route('/search')
def search():
    keyword = request.args.get('q', '')
    return keyword


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        f.save('uploads/' + secure_filename(f.filename))
        return 'Ok!'
    else:
        return '''
        <!doctype html>
        <title>Upload new File</title>
        <h1>Upload new File</h1>
        <form action="" method=post enctype=multipart/form-data>
          <p><input type=file name=file>
             <input type=submit value=Upload>
        </form>
        '''


@app.route('/cookies')
def hello_cookies():
    username = request.args.get('username')

    if username is None:
        username = request.cookies.get('username')
        response = make_response(render_template('hello.html', name=username))
    else:
        response = make_response(render_template('hello.html', name=username))
        response.set_cookie('username', username)

    return response


@app.route('/redirect/<url>')
def hello_redirect(url):
    try:
        to_url = url_for(url)
    except:
        abort(404)
    else:
        return redirect(to_url)


@app.route('/hello/index')
def hello_index():
    if 'username' in session:
        return 'Logged in as %s' % escape(session['username'])
    return redirect(url_for('hello_login'))


@app.route('/hello/login', methods=['GET', 'POST'])
def hello_login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('hello_index'))
    return '''
        <form action="" method="post">
            <p><input type="text" name="username"></p>
            <p><input type="submit" value="Login"></p>
        </form>
        '''


@app.route('/hello/logout')
def hello_logout():
    session.pop('username', None)
    app.logger.debug('Logout')  # logging
    return redirect(url_for('hello_login'))

# url_for('static', filename='style.css')  static/style.css
# os.urandom(20)
app.secret_key = '\xb5`\xeb+\xff\xc4\xae\xef+\x9c\x0bf?\xb0\xcdR\xfb%\x98\x05'

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
