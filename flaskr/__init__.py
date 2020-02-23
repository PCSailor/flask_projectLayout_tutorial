#! python3
import os
from flask import Flask

def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        # a default secret that should be overridden by instance config
        SECRET_KEY="dev",
        # store the database in the instance folder
        DATABASE=os.path.join(app.instance_path, "flaskr.sqlite"),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.update(test_config)
    
    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # A simple page that returns hello
    @app.route('/hello')
    def hello():
        return 'Hello World from __init__.py from within the flaskr app'

# From auth.py -> Place this code in the __init__.py file
# Import & register the auth.py blueprint from the factory app using app.register_blueprint().
# Place at end of factory function before returning the app
    def create_app():
        app = ...
        # existing code omitted
        from . import auth
        app.register_blueprint(auth.bp)
        return app
# END auth.py -> __init__.py code

# From db.py file, add this to the __init__.py file
# Import & call this function from the factory, placing at end of factory function before returning the app
    def create_app():
        app = ...
        # existing code omitted
        from . import db
        db.init_app(app)
        return app
    return app
# END db.py -> __init__.py code

# From blog.py file, add this to the flaskr/__init__.py file
# import & register blueprint from factory using app.register_blueprint()
# place code at end of factory before returning the app
def create_app():
	app = ...
	#existing code omitted
	from . import blog
	app.register_blueprint(blog.bp)
	app.add_url_rule('/', endpoint='index')
	return app
# END blog.py -> __init__.py code



'''
To Test:
# Terminal: 
#   export FLASK_APP=flaskr
#   export FLASK_ENV=development
#   flask run (NOT USED?= 'python3 -m flask run')
# in browser, open http://127.0.0.1:5000/hello 
#   should result: "Hello World from __init__.py from within the flaskr app"
#  Terminal: Ctrl C to quit flask run
'''