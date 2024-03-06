#!/usr/bin/env python3
# -----------------------------------------------------------------------------
# Project: SEES-Voting-App
# File: voting_app.py
# -----------------------------------------------------------------------------
# Purpose:
# This is the main entry point for the sees-voting-app. This file is used to
# create the Flask app and run the gunicorn web server.
#
# Copyright (C) 2024 GSECARS, The University of Chicago, USA
# This software is distributed under the terms of the MIT license.
# -----------------------------------------------------------------------------

import argparse
import subprocess
from sees_voting_app import create_flask_app
from sees_voting_app.utils import combine_results


app = create_flask_app()


def main() -> None:
    """Main entry point for the sees-voting-app."""
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="SEES Voting App")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug mode")
    parser.add_argument("-r", "--results", action="store_true", help="Combine results and generate a results.csv file.")
    args = parser.parse_args()

    # Combine results and generate a results.csv file
    if args.results:
        combine_results()
    # Run the Flask app
    elif args.debug:
        app.run(host="0.0.0.0", port=5000, debug=True)
    else:
        subprocess.run(["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "voting_app:app"])


if __name__ == "__main__":
    main()
