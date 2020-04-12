import os

from flask_api import FlaskAPI


def create_app():
    app = FlaskAPI(__name__)
    app.config.from_mapping(SECRET_KEY=os.environ.get("SECRET_KEY"))

    from . import api

    app.register_blueprint(api.bp)

    return app
