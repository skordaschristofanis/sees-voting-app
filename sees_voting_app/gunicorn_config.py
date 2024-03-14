#!/usr/bin/env python3
# -----------------------------------------------------------------------------
# Project: SEES-Voting-App
# File: gunicorn_config.py
# -----------------------------------------------------------------------------
# Purpose:
# This file is used to configure the gunicorn web server.
#
# Copyright (C) 2024 GSECARS, The University of Chicago, USA
# This software is distributed under the terms of the MIT license.
# -----------------------------------------------------------------------------

from sees_voting_app import db_session

# Gunicorn configuration
bind = "0.0.0.0:5000"
workers = 8
timeout = 60
graceful_timeout = 30
accesslog = "logs/gunicorn_access.log"
errorlog = "logs/gunicorn_error.log"


def post_fork(server, worker) -> None:
    """Post-fork server and worker initialization."""
    db_session.remove()


def post_worker_exit(server, worker) -> None:
    """Post-worker shutdown."""
    db_session.remove()
