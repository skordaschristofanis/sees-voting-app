#!/usr/bin/env python3
# -----------------------------------------------------------------------------
# Project: SEES-Voting-App
# File: config.py
# -----------------------------------------------------------------------------
# Purpose:
# This file is used to define the configuration settings for the Flask app.
#
# Copyright (C) 2024 GSECARS, The University of Chicago, USA
# This software is distributed under the terms of the MIT license.
# -----------------------------------------------------------------------------

import os
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dataclasses import dataclass, field
from dotenv import load_dotenv
from pathlib import Path
from typing import List


# Find the .env file in the parent directory
env_path = Path(__file__).resolve().parent.parent / "data" / ".env"

# Load the environment variables from the .env file
load_dotenv(env_path)


class Config:
    """A class that includes the configuration settings for the Flask app."""

    SECRET_KEY = os.getenv("SECRET_KEY")
    MAIL_SERVER = os.getenv("MAIL_SERVER")
    MAIL_PORT = os.getenv("MAIL_PORT")
    MAIL_USE_TLS = os.getenv("MAIL_USE_TLS")
    VOTING_ENDS = datetime.strptime(os.getenv("VOTING_ENDS"), "%Y-%m-%d %H:%M:%S")


@dataclass
class MailConfig:
    """A class that provides the sender address and mailing list."""

    _sender_address: str = field(init=False, compare=False, repr=False)
    _admin_mailing_list: str = field(init=False, compare=False, repr=False)

    def __post_init__(self) -> None:
        self._sender_address = os.getenv("MAIL_SENDER_ADDRESS")
        self._admin_mailing_list = os.getenv("ADMIN_MAILING_LIST").replace("[", "").replace("]", "").replace(" ", "")

    @property
    def sender_address(self) -> str:
        return self._sender_address.replace(" ", "")

    @property
    def admin_mailing_list(self) -> List[str]:
        return self._admin_mailing_list.split(",")


@dataclass
class DBConfig:
    """A class that provides the configuration settings for the database."""

    _database_uri: str = field(init=False, compare=False, repr=False)

    def __post_init__(self) -> None:
        self._database_uri = os.getenv("DATABASE_URI")

    @property
    def database_uri(self) -> str:
        return self._database_uri


def initialize_db():
    """Initialize the database."""
    db_config = DBConfig()
    db_engine = create_engine(db_config.database_uri, pool_size=10, max_overflow=2, pool_timeout=30)
    db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=db_engine))
    # Create a declarative base
    base = declarative_base()
    return db_config, db_engine, db_session, base
