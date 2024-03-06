#!/usr/bin/env python3
# -----------------------------------------------------------------------------
# Project: SEES-Voting-App
# File: utils.py
# -----------------------------------------------------------------------------
# Purpose:
# This file is used to define utility functions for the voting app. The
# functions are used to send confirmation emails to voters and to notify the
# admin group when a new vote is recorded.
#
# Copyright (C) 2024 GSECARS, The University of Chicago, USA
# This software is distributed under the terms of the MIT license.
# -----------------------------------------------------------------------------

import csv
import glob
import re
from flask_mailman import EmailMessage
from pathlib import Path
from typing import List

from sees_voting_app.voting_system import Voter


__all__ = ["combine_results"]


def send_comfirmation_email(sender_address, voter: Voter) -> None:
    """Send a confirmation email to the voter."""
    
    # Create the message
    msg = EmailMessage(
        subject="Voting Confirmation",
        from_email=sender_address,
        to=[voter.email],
    )

    # Set the selection string
    selections = "\n".join(
        [
            f"{selection.name}: <a href='{selection.bio_url}'>{selection.bio_url}</a><br>"
            for selection in voter.selections_list
        ]
    )

    # Set the body of the message
    msg.body = f"""
<html>
    <head>
        <body>
            <p>Hello {voter.full_name},</p>

            <p>Thank you for voting in the SEES election. Your vote has been recorded.</p>

            <p>Your selections are as follows:<br>
            {selections}</p>

            <p>This is an automated message. Please do not reply to this email.</p>

            <p>Best regards,<br>
            The SEES Team<br>
            <a href="mailto:sees_info@millenia.cars.aps.anl.gov">sees_info@millenia.cars.aps.anl.gov</a></p>
        </body>
    </head>
<html>
"""

    # Set the content type to HTML
    msg.content_subtype = "html"

    try:
        msg.send()
    except Exception as e:
        # Temporary catch-all exception handling until the mail is properly configured
        print(f"An error occurred while sending the email: {e}")


def send_vote_to_admin_group(
    sender_address, mailing_list: List[str], voter: Voter
) -> None:
    """Send the vote to the admin group."""

    # Create the selections string
    selections = "\n".join([f"{selection.name}" for selection in voter.selections_list])

    # Set the body of the message
    body = f"""Hello all,

A new vote has been recorded in the SEES election.

Voter details:
Full Name: {voter.full_name}
Email: {voter.email}
ORCID iD: {voter.orcid_id}

Selections:
{selections}

Best regards,
The SEES Team
"""

    # Create the message
    msg = EmailMessage(
        "New Vote for SEES election.",
        body,
        sender_address,
        mailing_list,
    )

    try:
        msg.send()
    except Exception as e:
        # Temporary catch-all exception handling until the mail is properly configured
        print(f"An error occurred while sending the email: {e}")


def combine_results() -> None:
    """Combine the results and generate a responses.csv file."""
    # Set the path to the combined CSV file
    combined_results_csv = Path(__file__).parent.parent / "data" / "responses.csv"

    # Get a list of all the CSV files
    csv_files = glob.glob(str(Path(__file__).parent.parent / "data" / "*.csv"))

    # Write the header to the combined CSV file
    with open(combined_results_csv, "w") as file:
        writer = csv.writer(file)
        writer.writerow(["FullName", "Email", "ORCIDiD", "Pref1", "Pref2", "Pref3", "Pref4", "Pref5"])

    # Append the data from each CSV file to the combined CSV file
    for csv_file in csv_files:
        # Skip files that do not start with an ORCID iD
        if not re.match(r".*/\d{4}-\d{4}-\d{4}-\d{3}[0-9X]\_.*\.csv", csv_file):
            continue

        if csv_file == str(combined_results_csv):
            continue
        with open(csv_file, "r") as file:
            next(file)  # Skip the header
            with open(combined_results_csv, "a") as combined_file:
                for line in file:
                    combined_file.write(line)
