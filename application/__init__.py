from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_ckeditor import CKEditor
from flask_login import LoginManager
from flask_gravatar import Gravatar
from flask_mail import Mail
from application.config import Config


##CONNECT TO DB
db = SQLAlchemy()
# db.create_all()

login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'alert-warning'
mail = Mail()

ckeditor = CKEditor()
bootstrap = Bootstrap()

# initializing gravatar
gravatar = Gravatar(size=50,
                    rating='g',
                    default='retro',
                    force_default=False,
                    force_lower=False,
                    use_ssl=False,
                    base_url=None)


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    login_manager.init_app(app)
    ckeditor.init_app(app)
    mail.init_app(app)
    gravatar.init_app(app)
    bootstrap.init_app(app=app)

    from application.users.routes import users
    from application.posts.routes import posts
    from application.main.routes import main
    from application.errors.handlers import errors
    app.register_blueprint(posts)
    app.register_blueprint(users)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app