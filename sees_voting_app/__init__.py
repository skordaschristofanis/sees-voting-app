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
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from sees_voting_app.config import Config, MailConfig
from sees_voting_app.config import DBConfig
from sqlalchemy.ext.declarative import declarative_base


__all__ = ["create_flask_app"]


# Create a Mail instance
mail = Mail()
# Get the sender address and admin mailing list
mail_config = MailConfig()
sender_address = mail_config.sender_address
admin_mailing_list = mail_config.admin_mailing_list
# Create a SQLAlchemy engine and session
db_config = DBConfig()
db_engine = create_engine(db_config.database_uri, pool_size=20, max_overflow=10, pool_timeout=30)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=db_engine))
# Create a declarative base
Base = declarative_base()


def create_flask_app(config_class=Config) -> Flask:
    """Create a Flask app using the provided configuration class."""
    # Create the Flask app
    app = Flask(__name__)
    app.config.from_object(config_class)

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
