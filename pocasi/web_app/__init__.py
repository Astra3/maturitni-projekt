from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

from pocasi import pocasi_data

secret_key_env_var = "POCASI_APLIKACE_WEB"
from pocasi.web_app.config import Config

if pocasi_data is not None:
    max_date = str(pocasi_data.iloc[-1].name.date())
    min_date = str(pocasi_data.iloc[0].name.date())
else:
    max_date = None
    min_date = None

bcrypt = Bcrypt()

login_manager = LoginManager()
login_manager.login_message = "Pro přístup na tuhle stránku musíte být přihlášen!"
login_manager.login_message_category = "warning"
login_manager.login_view = "main.login"


def create_app():
    app = Flask(__name__)

    app.jinja_env.globals.update(zip=zip, enumerate=enumerate, min_date=min_date, max_date=max_date)
    app.config.from_object(Config)

    bcrypt.init_app(app)
    login_manager.init_app(app)

    from pocasi.web_app.main.routes import main
    from pocasi.web_app.render.routes import render
    from pocasi.web_app.request.routes import request_blueprint

    app.register_blueprint(main)
    app.register_blueprint(render)
    app.register_blueprint(request_blueprint)

    return app
