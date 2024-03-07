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

from flask import Blueprint, render_template, request, redirect

from sees_voting_app import sender_address, admin_mailing_list
from sees_voting_app.forms import VoteForm
from sees_voting_app.voting_system import Voter, VotingSystem
from sees_voting_app.utils import send_comfirmation_email, send_vote_to_admin_group


# Create a Blueprint for the voting routes
voting = Blueprint("voting", __name__)


@voting.route("/", methods=["GET", "POST"])
def vote():
    """Display the voting form and process the vote."""

    # Create a form instance of the VoteForm
    form = VoteForm()
    # Get the list of candidates and set the choices for the form
    voting_system = VotingSystem()
    form.set_candidate_choices(voting_system.candidates)

    if form.validate_on_submit():
        
        # Check if the orcid_id is already in the database
        if voting_system.orcid_exists(orcid_id=request.form.get("orcid_id")):
            print("The ORCID iD is already in the database.")
            return redirect("https://seescience.org/")
        
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
        voter.selection_5 = request.form.get("selection_5")

        # Record the vote
        voting_system.record_vote(voter=voter, candidates=voting_system.candidates)

        # Send a confirmation email
        if request.form.get("send_email"):
            send_comfirmation_email(sender_address=sender_address, voter=voter)

        # Notify the admin group
        send_vote_to_admin_group(sender_address=sender_address, mailing_list=admin_mailing_list, voter=voter)

        # Thank the voter for voting
        return redirect("https://seescience.org/")

    return render_template("vote.html", form=form)
