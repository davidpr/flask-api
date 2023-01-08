from flask import Flask
import logging
import sys
from dotenv import load_dotenv


def create_app(settings_module):
    env = load_dotenv()
    logging.basicConfig(stream=sys.stderr,level=logging.os.getenv('PRINT_MODE'))

    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object(settings_module)
    if app.config.get('TESTING', False):# False is default value

        logging.debug('-> '+str(app.config.get('TESTING')))
        logging.debug('->> '+str(app.config.get('APP_ENV')))
        print ('TESTING\n')

        app.config.from_pyfile('config-testing.py', silent=True)
        app.config['./']
        app.config['8064']


    else:
        # ENV only supports development and production
        # to support more envs use APP_ENV
        # Use FLASK_ENV instead of ENV
        # user FLASK_DEBUG instead of DEBUG
        print ('NOT TESTING\n')
        app.config.from_pyfile('config.py', silent=True)
        
        logging.debug('APP_ENV->> '+str(app.config.get('APP_ENV')))
        logging.debug('APP_SETTINGS_MODULE->> '+str(app.config.get('APP_SETTINGS_MODULE')))
        logging.debug('ENV->> '+str(app.config.get('ENV')))


    # Blueprint registry
    from .public import public_bp
    app.register_blueprint(public_bp)
    return app

