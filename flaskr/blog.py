#! python3
# blog.py
# This defines the blueprint & registers it in application factory
# NOTE: Code to enter into __init__.py file below

from flask import (
Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('blog', __name__)

# Now to import & register the blueprint from the factory using app.register_blueprint()
# place this code at end of factory before returning the app
# add to flaskr/__init__.py file
"""def create_app():
	app = ...
	#existing code omitted
	from . import blog
	app.register_blueprint(blog.bp)
	app.add_url_rule('/', endpoint='index')
	return app"""

# Index will show all of the posts, most recent first
# JOIN is used so author info from USER table is available in result
@bp.route('/')
def index():
    db = get_db()
    posts = db.excute(
		'SELECT p.id, title, body, created, author_id, username'
		' FROM post p JOIN user u ON p.author_id = u.id'
		' ORDER BY created DESC'
	).fetchall()
	return render_template('blog/index.html', posts=posts)

# create
@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
	if request.method == 'POST':
		title = request.form['title']
		body = request.form['body']
		error = None
		