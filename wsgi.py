#!/usr/bin/env python3
# -----------------------------------------------------------------------------
# Project: SEES-Voting-App
# File: wsgi.py
# -----------------------------------------------------------------------------
# Purpose:
# This is the main entry point for the sees-voting-app. This file is used to
# create the Flask app and run the gunicorn web server.
#
# Copyright (C) 2024 GSECARS, The University of Chicago, USA
# This software is distributed under the terms of the MIT license.
# -----------------------------------------------------------------------------

import subprocess
from sees_voting_app import create_flask_app


app = create_flask_app()


if __name__ == "__main__":
    subprocess.run(["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "wsgi:app"])
