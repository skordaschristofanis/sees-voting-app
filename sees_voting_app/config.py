#!/usr/bin/env python3
# -----------------------------------------------------------------------------
# Project: SEES-Voting-App
# File: config.py
# -----------------------------------------------------------------------------
# Purpose:
# This file is used to define the configuration settings for the Flask app.
#
# Copyright (C) 2024 GSECARS, The University of Chicago, USA
# This software is distributed under the terms of the MIT license.
# -----------------------------------------------------------------------------

import os
from dataclasses import dataclass, field
from dotenv import load_dotenv
from pathlib import Path
from typing import List


# Find the .env file in the parent directory
env_path = Path(__file__).resolve().parent.parent / "data" / ".env"

# Load the environment variables from the .env file
load_dotenv(env_path)


class Config:
    """A class that includes the configuration settings for the Flask app."""
    SECRET_KEY = os.getenv("SECRET_KEY")
    MAIL_SERVER = os.getenv("MAIL_SERVER")
    MAIL_PORT = os.getenv("MAIL_PORT")
    MAIL_USE_TLS = os.getenv("MAIL_USE_TLS")


@dataclass
class MailConfig:
    """A class that provides the sender address and mailing list."""
    _sender_address: str = field(init=False, compare=False, repr=False)
    _admin_mailing_list: str = field(init=False, compare=False, repr=False)

    def __post_init__(self) -> None:
        self._sender_address = os.getenv("MAIL_SENDER_ADDRESS")
        self._admin_mailing_list = os.getenv("ADMIN_MAILING_LIST").replace("[", "").replace("]", "").replace(" ", "")

    @property
    def sender_address(self) -> str:
        return self._sender_address.replace(" ", "")
    
    @property
    def admin_mailing_list(self) -> List[str]:
        return self._admin_mailing_list.split(",")
