from flask import Flask, Blueprint
from flask.ext.bootstrap import Bootstrap
from flask.ext.babel import Babel
from flask.ext.mail import Mail
from flask.ext.moment import Moment
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.user import UserManager, UserMixin, SQLAlchemyAdapter
from flask.ext.admin import Admin
from flask.ext.admin.base import AdminIndexView, expose
from flask.ext.user import current_user
from flask_wtf.csrf import CsrfProtect
from config import config
import chartkick

class AdminView(AdminIndexView):
    @expose('/')
    def index(self):
        return self.render('admin/index.html')

    def is_accessible(self):
        return current_user.is_authenticated()

bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()
babel = Babel()
csrf = CsrfProtect()
admin = Admin(index_view=AdminView())

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    babel.init_app(app)
    admin.init_app(app)
    csrf.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .user import user as user_blueprint
    app.register_blueprint(user_blueprint)

    ck = Blueprint('ck_page', __name__, static_folder=chartkick.js(), static_url_path='/static')
    app.register_blueprint(ck, url_prefix='/ck')
    app.jinja_env.add_extension("chartkick.ext.charts")

    return app

