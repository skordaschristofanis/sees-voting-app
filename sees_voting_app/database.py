#!/usr/bin/env python3
# -----------------------------------------------------------------------------
# Project: SEES-Voting-App
# File: database.py
# -----------------------------------------------------------------------------
# Purpose:
# This file is used to define the database configuration and the database
# models for the SEES election voting app.
#
# Copyright (C) 2024 GSECARS, The University of Chicago, USA
# This software is distributed under the terms of the MIT license.
# -----------------------------------------------------------------------------

from contextlib import contextmanager
from sqlalchemy import Column, Integer, String, DateTime, UniqueConstraint

from sees_voting_app import Base, initialize_db

# Move the global declaration to the top
global db_session
db_session = None


# Add a context manager for the session
@contextmanager
def session_scope():
    """Return a session scope for the database."""
    global db_session
    if db_session is None:
        db_config, db_engine, db_session, Base = initialize_db()
    session = db_session()
    try:
        yield session
        session.commit()
    finally:
        session.close()


class VoteModel(Base):
    __tablename__ = "votes"

    id = Column(Integer, primary_key=True)
    full_name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    orcid_id = Column(String(255), nullable=False, unique=True)
    selection_1 = Column(String(255), nullable=False)
    selection_2 = Column(String(255), nullable=False)
    selection_3 = Column(String(255), nullable=False)
    selection_4 = Column(String(255), nullable=False)
    timestamp = Column(DateTime, nullable=False)

    __table_args__ = (UniqueConstraint("email", "orcid_id", name="unique_email_orcid"),)


class DBException(Exception):

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message}"
