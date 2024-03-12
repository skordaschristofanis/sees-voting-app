#!/usr/bin/env python3
# -----------------------------------------------------------------------------
# Project: SEES-Voting-App
# File: forms.py
# -----------------------------------------------------------------------------
# Purpose:
# This file is used to define the form for the ranking vote. The form is
# created using the Flask-WTF extension and includes fields for the user's
# full name, email, ORCID iD, and the candidates they are voting for.
#
# Copyright (C) 2024 GSECARS, The University of Chicago, USA
# This software is distributed under the terms of the MIT license.
# -----------------------------------------------------------------------------

from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, Regexp

from sees_voting_app.voting_system import Candidate


def NoDefaultRequired(form, field) -> None:
    """Validator to ensure that the default option is not selected."""
    if field.data == "None":
        raise ValidationError("Please select a candidate.")


class VoteForm(FlaskForm):
    """Form template for the ranking vote."""

    full_name = StringField("Your Full Name", validators=[DataRequired()])
    email = StringField("Your Email", validators=[DataRequired(), Email()])
    orcid_id = StringField(
        "Your ORCID ID (16-digit number)",
        validators=[
            DataRequired(),
            Regexp(
                r"^\d{4}-\d{4}-\d{4}-\d{3}[0-9X]$",
                message="Please enter a valid ORCID iD (e.g. 0000-0000-0000-0000)",
            ),
        ],
    )
    selection_1 = SelectField("Choice 1", validators=[DataRequired(), NoDefaultRequired], choices=[])
    selection_2 = SelectField("Choice 2", choices=[])
    selection_3 = SelectField("Choice 3", choices=[])
    selection_4 = SelectField("Choice 4", choices=[])
    send_email = BooleanField("Send a confirmation email", default="checked")
    submit = SubmitField("Submit Your Vote")

    def set_candidate_choices(self, candidates: list[Candidate]) -> None:
        """Set the choices for the form."""
        default_choice = ("None", "Select a candidate...")
        choices = [default_choice] + [(candidate.name, candidate.name) for candidate in candidates]
        self.selection_1.choices = choices
        self.selection_2.choices = choices
        self.selection_3.choices = choices
        self.selection_4.choices = choices
