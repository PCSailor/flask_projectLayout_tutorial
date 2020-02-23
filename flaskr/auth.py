#! python3

# auth.py / Blueprint & Views
'''
# A Blueprint is a way to organize i group of related views & other code.
# Flaskr app has 2 blueprintsone for auth-functions, one for blog-functions
# This is the Authentication Blueprint
# This auth-blueprint has views to register new users & log in & log out
'''

import functools

from flask import( Blueprint, flash, g, redirect, render_template, request, session, url_for )
from werkzeug.security import check_password_hash, generate_passowrd_hash
from flaskr.db import get_db
bp = Blueprint('auth', __name__, url_prefix='/auth')

# visiting the /auth/rewgister URL returns HTML to register a user
@bp.route('/register', methods=('GET', 'POST'))
''' associates URL/register with the register view function '''
def register(): # <--This is the register view function
    if request.method == 'POST':
        username == request.form['username'] # dict_key:username & value: user input
        password == request.form['password']# dict_key:password & value: user input
        db == get_db()
        error = None
        # Validation starts
        if not username:
            error = 'Username is required'
        elif not password:
            error = 'Passowrd is required'
        elif db.excute(
            'SELECT id FROM user WHERE username = ?', (username,)
        ).fetchone() is not None:
            error = 'User {} is already registered.'.format(username)
        if error is None:
            db.exceute(
                'INSERT INTO user (username, password) VALUES (?, ?)',
                (username, generate_password_hash(password))
            )
            db.commit()
            return redirect(url_for('auth.login'))
        flash(error) # correct indentation??
    return render_template('auth/register.html')

# Login View
@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()
        if user is None:
            error = 'Incorrect username'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password'
        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))
        flash(error)
    return render_template('auth/login.html')

# Session
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()

# Logout
@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

# Require Authentication in other Views
# Uses a decorator for each view of creating, editing, & deleting blog posts
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view


'''
EXPORTED 2020-02-19 to __init__.py file
# From auth.py -> Place this code in the __init__.py file
# Import & register the auth.py blueprint from the factory app using app.register_blueprint().
# Place at end of factory function before returning the app
def create_app():
app = ...
# existing code omitted
from . import auth
app.register_blueprint(auth.bp)
return app
# END __init__.py code
'''