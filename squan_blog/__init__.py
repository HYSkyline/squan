# -*- coding:utf-8 -*-

from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from flask_login import LoginManager
from config import config
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class

bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()
geo_engine = create_engine('postgresql://postgres:625383@localhost/squan_blog', echo=True)
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'

avatars = UploadSet('avatars', IMAGES)


def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)

    login_manager.init_app(app)

    from .main import main as main_blueprint
    from .auth import auth as auth_blueprint
    from .api import api as api_blueprint
    from .quiz import quiz as quiz_blueprint
    from .geo import geo as geo_blueprint
    app.register_blueprint(main_blueprint)
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(api_blueprint, url_prefix='/api')
    app.register_blueprint(quiz_blueprint, url_prefix='/quiz')
    app.register_blueprint(geo_blueprint, url_prefix='/geo')

    configure_uploads(app, avatars)
    patch_request_class(app, 4194304)

    return app
