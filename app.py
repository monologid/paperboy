import config
from flask import Flask
from flask_cors import CORS
from controllers.index import root
from controllers.api.job import api_job_v1

conf = config.Config()


def initialize_app():
    app = Flask(
        __name__,
        instance_relative_config=False,
        static_url_path='',
        static_folder='templates/dist',
        template_folder='templates/dist'
    )
    CORS(app)
    app.config.from_object(f"config.{conf.ENV.capitalize()}")

    app.register_blueprint(root)
    app.register_blueprint(api_job_v1)

    with app.app_context():
        return app
