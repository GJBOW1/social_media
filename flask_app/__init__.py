from flask import Flask
from flask_app.config.config import Config
from flask_app.models import weather_api
app = Flask(__name__)
app.secret_key = "Not all who wonder are lost."


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Register Blueprints
    from .models import weather_bp
    app.register_blueprint(weather_bp) # No url_prefix here if already set in Blueprint

    # You can also set up logging here if needed
    # import logging
    # if not app.debug:
    #     # For production logging
    #     pass
    # else:
    #     # For development logging
    #     app.logger.setLevel(logging.INFO)

    return app