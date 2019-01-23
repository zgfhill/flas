import os
import click
from flask_migrate import Migrate, upgrade
from app import create_app, db
from app.models import User, Role, Post, Follow

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)

@app.shell_context_processor
def make_shell_context():
	return dict(db=db, User=User, Role=Role, Post=Post)

@app.cli.command()
def test():
	'''RUn the unit tests'''
	import unittest
	tests = unittest.TestLoader().discover('tests')
	unittest.TextTestRunner(verbosity=2).run(tests)

@app.cli.command()
@click.option('--length', default=25, help='Number of functions to include in the profiler report.')
@click.option('--profile-dir', default=None, help='Directory whree profiler data files are saved.')
def profile(length, profile_dir):
	'''Start the application under the code profiler.'''
	from werkzeug.contrib.profiler import ProfilerMiddleware
	app.wsgi_app = ProfileMiddleware(app.wsgi_app, restrictions=[length], profile_dir=profile_dir)
	app.run(debug=False)
