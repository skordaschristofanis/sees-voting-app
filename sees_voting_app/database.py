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
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

from sees_voting_app.config import DBConfig


# Create a SQLAlchemy engine and session
db_config = DBConfig()
db_engine = create_engine(db_config.database_uri)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=db_engine))

# Create a declarative base
Base = declarative_base()


# Add a context manager for the session
@contextmanager
def session_scope():
    """Return a session scope for the database."""
    session = db_session()
    try:
        yield session
        session.commit()
    finally:
        session.close()


class VoteModel(Base):
    __tablename__ = 'votes'

    id = Column(Integer, primary_key=True)
    full_name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    orcid_id = Column(String(255), nullable=False)
    selection_1 = Column(String(255), nullable=False)
    selection_2 = Column(String(255), nullable=False)
    selection_3 = Column(String(255), nullable=False)
    selection_4 = Column(String(255), nullable=False)
    timestamp = Column(String(255), nullable=False)
