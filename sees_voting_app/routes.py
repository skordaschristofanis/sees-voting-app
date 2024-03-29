#!/usr/bin/env python3
# -----------------------------------------------------------------------------
# Project: SEES-Voting-App
# File: routes.py
# -----------------------------------------------------------------------------
# Purpose:
# This file is used to define the routes for the voting app. The voting route
# displays the voting form and processes the vote. The vote is recorded using
# the VotingSystem class and the voter is notified by email if requested.
#
# Copyright (C) 2024 GSECARS, The University of Chicago, USA
# This software is distributed under the terms of the MIT license.
# -----------------------------------------------------------------------------

from flask import Blueprint, render_template, request, flash
from datetime import datetime

from sees_voting_app import sender_address, admin_mailing_list, vote_logger, voting_ends
from sees_voting_app.database import DBException
from sees_voting_app.forms import VoteForm
from sees_voting_app.voting_system import Voter, VotingSystem
from sees_voting_app.utils import send_comfirmation_email, send_vote_to_admin_group, send_database_error_email
from sees_voting_app.config import initialize_db

global db_config, db_engine, db_session, base
db_config = db_engine = db_session = base = None

# Create a Blueprint for the voting routes
voting = Blueprint("voting", __name__)


@voting.route("/", methods=["GET", "POST"])
def vote():
    """Display the voting form and process the vote."""
    global db_config
    if db_config is None:
        db_config, db_engine, db_session, base = initialize_db()
    # Create a form instance of the VoteForm
    form = VoteForm()
    # Get the list of candidates and set the choices for the form
    voting_system = VotingSystem()
    form.set_candidate_choices(voting_system.candidates)

    # Check if the voting period has ended
    voting_ended = datetime.now() >= voting_ends

    if voting_ended:
        flash(
            """
            <p>The voting period has ended. We are no longer accepting votes. If you have any questions or concerns, please do not hesitate to contact us at <a href="mailto:sees_info@millenia.cars.aps.anl.gov">sees_info@millenia.cars.aps.anl.gov</a>.</p>
            """,
            "danger",
        )
        return render_template('vote.html', form=form, voting_ended=voting_ended)

    if form.validate_on_submit():

        # Check if the voting period has ended
        if datetime.now() > voting_ends:
            flash(
                """
                <h4>Failure to Submit the Vote</h4>
                <p>The voting period has ended. We are no longer accepting votes. If you have any questions or concerns, please do not hesitate to contact us at <a href="mailto:sees_info@millenia.cars.aps.anl.gov">sees_info@millenia.cars.aps.anl.gov</a>.</p>
                """,
                "danger",
            )
            return render_template("vote.html", form=form, voting_ended=voting_ended)

        try:
            # Check if the orcid_id is already in the database
            if voting_system.orcid_exists(orcid_id=request.form.get("orcid_id")):
                print(f"The ORCID iD {request.form.get('orcid_id')} is already in the database.")
                vote_logger.warning(f"The ORCID iD {request.form.get('orcid_id')} is already in the database.")
                flash(
                    """
                    <h4>Failure to Submit the Vote</h4>
                    <p>The provided ORCID iD is already in use. Please check that your ORCID iD is correct. If you continue to experience issues or have any concerns, please do not hesitate to contact us at <a href="mailto:sees_info@millenia.cars.aps.anl.gov">sees_info@millenia.cars.aps.anl.gov</a>.</p>
                    """,
                    "danger",
                )
                return render_template("vote.html", form=form, voting_ended=voting_ended)
        except DBException as e:
            send_database_error_email(sender_address=sender_address, mailing_list=admin_mailing_list, error=e.message)

        try:
            # Check if the email is already in the database
            if voting_system.email_exists(email=request.form.get("email")):
                print(f"The email address {request.form.get('email')} is already in the database.")
                vote_logger.warning(f"The email address {request.form.get('email')} is already in the database.")
                flash(
                    """
                    <h4>Failure to Submit the Vote</h4>
                    <p>The provided email address is already in use. Please check that your email address is correct. If you continue to experience issues or have any concerns, please do not hesitate to contact us at <a href="mailto:sees_info@millenia.cars.aps.anl.gov">sees_info@millenia.cars.aps.anl.gov</a>.</p>
                    """,
                    "danger",
                )
                return render_template("vote.html", form=form, voting_ended=voting_ended)
        except DBException as e:
            send_database_error_email(sender_address=sender_address, mailing_list=admin_mailing_list, error=e.message)

        # Create a Voter instance
        voter = Voter()

        # Process the vote
        voter.full_name = request.form.get("full_name")
        voter.email = request.form.get("email")
        voter.orcid_id = request.form.get("orcid_id")
        voter.selection_1 = request.form.get("selection_1")
        voter.selection_2 = request.form.get("selection_2")
        voter.selection_3 = request.form.get("selection_3")
        voter.selection_4 = request.form.get("selection_4")

        # Record the vote
        voting_system.record_vote(voter=voter)
        try:
            voting_system.record_vote_to_db(voter=voter)
        except DBException as e:
            send_database_error_email(sender_address=sender_address, mailing_list=admin_mailing_list, error=e.message)

        # Send a confirmation email
        if request.form.get("send_email"):
            send_comfirmation_email(sender_address=sender_address, voter=voter)

        # Notify the admin group
        send_vote_to_admin_group(sender_address=sender_address, mailing_list=admin_mailing_list, voter=voter)

        # Thank the voter for voting
        flash(
            """
            <h4>Vote Submitted Successfully</h4>
            <p>Your vote has been recorded. Thank you for your participation. If you have any questions or concerns, please do not hesitate to contact us at <a href="mailto:sees_info@millenia.cars.aps.anl.gov">sees_info@millenia.cars.aps.anl.gov</a>.</p>
            """,
            "success",
        )

        return render_template("vote.html", form=form, voting_ended=voting_ended)

    return render_template("vote.html", form=form, voting_ended=voting_ended)
