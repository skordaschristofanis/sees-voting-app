#!/usr/bin/env python3
# -----------------------------------------------------------------------------
# Project: SEES-Voting-App
# File: __init__.py
# -----------------------------------------------------------------------------
# Purpose:
# This is the main entry point for the sees-voting-app. This file is used to
# configure the Flask app and initialize the Mail instance.
#
# Copyright (C) 2024 GSECARS, The University of Chicago, USA
# This software is distributed under the terms of the MIT license.
# -----------------------------------------------------------------------------

import logging
from flask import Flask
from flask_mailman import Mail
from logging.handlers import RotatingFileHandler
from pathlib import Path

from sees_voting_app.config import Config, MailConfig, initialize_db


__all__ = ["create_flask_app"]


# Create a Mail instance
mail = Mail()
# Get the sender address and admin mailing list
mail_config = MailConfig()
sender_address = mail_config.sender_address
admin_mailing_list = mail_config.admin_mailing_list

# Initialize the database
db_config, db_engine, db_session, Base = initialize_db()

# Create the logs directory if it doesn't exist
Path("logs").mkdir(exist_ok=True)
# Set up vote logging
vote_logger = logging.getLogger("vote")
vote_logger.setLevel(logging.INFO)
vote_handler = RotatingFileHandler("logs/sees_voting_app.log", maxBytes=512 * 1024 * 1024, backupCount=1000000)
vote_handler.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | %(message)s"))
vote_logger.addHandler(vote_handler)
# Set up flask logging
flask_logger = logging.getLogger("werkzeug")
flask_logger.setLevel(logging.INFO)
flask_handler = RotatingFileHandler("logs/flask.log", maxBytes=512 * 1024 * 1024, backupCount=1000000)
flask_handler.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | %(message)s"))
flask_logger.addHandler(flask_handler)


def create_flask_app(config_class=Config) -> Flask:
    """Create a Flask app using the provided configuration class."""
    # Create the Flask app
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Set the flask logger
    app.logger = flask_logger

    # Initialize the Mail instance
    mail.init_app(app)

    # Create all tables in the database
    Base.metadata.create_all(bind=db_engine)

    # Import and register the voting blueprint
    from sees_voting_app.routes import voting

    app.register_blueprint(voting)

    # Add a teardown app context to remove the database session after each request
    @app.teardown_appcontext
    def cleanup(response_or_exception):
        db_session.remove()

    return app
