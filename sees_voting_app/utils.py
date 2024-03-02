from flask_mail import Message
from typing import List

from sees_voting_app import mail
from sees_voting_app.voting_system import Voter


def send_comfirmation_email(sender_address, voter: Voter) -> None:
    """Send a confirmation email to the voter."""

    # Create the message
    msg = Message(
        "Voting Confirmation",
        sender=sender_address,
        recipients=[voter.email],
    )

    # Set the selection string
    selections = "\n".join(
        [
            f"{selection.name}: {selection.bio_url}"
            for selection in voter.selections_list
        ]
    )

    # Set the body of the message
    msg.body = f"""Hello {voter.full_name},

Thank you for voting in the SEES election. Your vote has been recorded.

Your selections are as follows:
{selections}

This is an automated message. Please do not reply to this email.

Best regards,
The SEES Team
mailto:sees_info@millenia.cars.aps.anl.gov
"""
    try:
        mail.send(msg)
    except Exception as e:
        # Temporary catch-all exception handling until the mail is properly configured
        print(f"An error occurred while sending the email: {e}")


def send_vote_to_admin_group(
    sender_address, mailing_list: List[str], voter: Voter
) -> None:
    """Send the vote to the admin group."""

    # Create the message
    msg = Message(
        "New Vote for SEES election.",
        sender=sender_address,
        recipients=mailing_list,
    )

    # Create the selections string
    selections = "\n".join([f"{selection.name}" for selection in voter.selections_list])

    # Set the body of the message
    msg.body = f"""Hello all,

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
    try:
        mail.send(msg)
    except Exception as e:
        # Temporary catch-all exception handling until the mail is properly configured
        print(f"An error occurred while sending the email: {e}")
