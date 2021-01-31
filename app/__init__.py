from flask import Flask, render_template
from flask_login import LoginManager
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from config import DevConfig
from flask_uploads import UploadSet, IMAGES, configure_uploads

db = SQLAlchemy()
login_manager = LoginManager()
sess = Session()
images = ""

def page_not_found(e):
    return render_template('404.html'), 404


def internal_server_error(e):
    return render_template('500.html'), 500


def create_app(config_class=DevConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)
    global images
    images = UploadSet('image', IMAGES)
    app.config['UPLOADED_IMAGE_DEST'] = 'static/images'
    configure_uploads(app, images)
    db.init_app(app)
    login_manager.init_app(app)

    # The following is needed if you want to map classes to an existing database
    # with app.app_context():
    #     db.Model.metadata.reflect(db.engine)

    from populate_db import populate_db
    from app.models import Member  # , Art, Artist, ContributingArtists, Subscriptions, Events, Portfolio
    with app.app_context():
        db.create_all()
        populate_db()
    # Register Blueprints
    from app.main.routes import bp_main
    app.register_blueprint(bp_main)

    from app.auth.routes import bp_auth
    app.register_blueprint(bp_auth)

    return app
