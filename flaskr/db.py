#! python3

import sqlite3
import click
from flask import current_app, g
from flask.cli import with_appcontext

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    db=g.pop('db', None)
    if db is not None:
        db.close()

# Python functions that run SQL commands to the db.py file
def init_db():
    # get_db() returns a db connectionused to execute commands read from file
    db = get_db()
    # open.resoure() opens a file relative to flaskr package, useful since location where deployiong the app is unknown
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

# Define a command line called init-db which calls the init_db function showing a success user message
@click.command('init-db')
@with_appcontext
# close_db & init_db_command functions register with the app instance as a function taking an app & registering
def init_db_command():
    ''' Clear the existing data & create new tables '''
    init_db()
    click.echo('Initialized the database')

def init_app(app):
    # After returning response, Flask calls this function when cleaning up
    app.teardown_appcontext(close_db)
    # adds new command which can be called with Flask command
    app.cli.add_command(init_db_command)

'''
# Initialize the Database file
This registers init-db with the app, so it can be called using the flask command (similar to the previous flask-RUN COMMAND)
Note: If flask server is still running, either stop it or run this from a new terminal
  -If run from a new terminal, change dir, activate venv, set FLASK_APP, & set FLASK_ENV
Once done, in terminal, run the init-db command to initialize the database:
    flask init-db
There should now be a flaskr.sqlite file in the project's instance directory
'''