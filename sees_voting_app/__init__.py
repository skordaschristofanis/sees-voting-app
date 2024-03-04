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

from flask import Flask
from flask_mailman import Mail

from sees_voting_app.config import Config, MailConfig


__all__ = ["create_flask_app"]

# Create a Mail instance
mail = Mail()
# Get the sender address and admin mailing list
mail_config = MailConfig()
sender_address = mail_config.sender_address
admin_mailing_list = mail_config.admin_mailing_list


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
