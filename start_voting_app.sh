#!/bin/bash
# -----------------------------------------------------------------------------
# Project: SEES-Voting-App
# File: start_voting_app.sh
# -----------------------------------------------------------------------------
# Purpose:
# This script is used to start the SEES-Voting-App web application.
#
# Copyright (C) 2024 GSECARS, The University of Chicago, USA
# This software is distributed under the terms of the MIT license.
# -----------------------------------------------------------------------------

source /usr/share/anaconda3/bin/activate
conda activate votingAppENV
nohup python /usr/share/sees-voting-app/voting_app.py > /dev/null 2>&1 &
