from flask import Flask
from flask_mail import Mail

from sees_voting_app.config import Config


__all__ = ["create_flask_app"]

# Create a Mail instance
mail = Mail()


def create_flask_app(config_class=Config) -> Flask:
    """Create a Flask app using the provided configuration class."""
    # Create the Flask app
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize the Mail instance
    mail.init_app(app)

    # Import and register the voting blueprint
    from sees_voting_app.routes import voting

    app.register_blueprint(voting)

    return app
