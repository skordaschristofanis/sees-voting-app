#!/usr/bin/env python3
# -----------------------------------------------------------------------------
# Project: SEES-Voting-App
# File: voting_system.py
# -----------------------------------------------------------------------------
# Purpose:
# This file is used to define the voting system for the SEES election. The
# Candidate class is used to represent a candidate and their bio URL. The Voter
# class is used to represent a voter and their selections. The VotingSystem class
# is used to manage the ranking voting system and record the votes.
#
# Copyright (C) 2024 GSECARS, The University of Chicago, USA
# This software is distributed under the terms of the MIT license.
# -----------------------------------------------------------------------------

import csv
import logging
from datetime import datetime
from dataclasses import dataclass, field
from pathlib import Path
from typing import List

from sees_voting_app import vote_logger
from sees_voting_app.database import VoteModel, session_scope, DBException


__all__ = ["Candidate", "Voter", "VotingSystem"]


@dataclass
class Candidate:
    """A class to represent a candidate."""

    name: str = field(compare=False, repr=False)
    bio_url: str = field(compare=False, repr=False)


@dataclass
class Voter:
    """A class to represent a voter and their selections."""    
    _timestamp: str = field(init=False, compare=False, repr=False, default=datetime.now().strftime("%Y.%m.%d_%H.%M.%S"))

    selections_list: List[Candidate] = field(
        compare=False, repr=False, default_factory=list
    )
    full_name: str = field(init=False, compare=False, repr=False)
    email: str = field(init=False, compare=False, repr=False)
    orcid_id: str = field(init=False, compare=False, repr=False)
    selection_1: str = field(init=False, compare=False, repr=False)
    selection_2: str = field(init=False, compare=False, repr=False)
    selection_3: str = field(init=False, compare=False, repr=False)
    selection_4: str = field(init=False, compare=False, repr=False)

    def prepare_data(self, candidates: List[Candidate]) -> List[str]:
        # Prepare the data format
        data = [
            self.full_name,
            self.email,
            self.orcid_id,
            self.selection_1,
            self.selection_2,
            self.selection_3,
            self.selection_4,
        ]

        # Populate the voter's selections with the candidate names
        selections = [
            self.selection_1,
            self.selection_2,
            self.selection_3,
            self.selection_4,
        ]
        for selection in selections:
            if selection == "None":
                continue
            for candidate in candidates:
                if selection == candidate.name:
                    self.selections_list.append(candidate)

        return data

    @property
    def timestamp(self) -> str:
        return self._timestamp


@dataclass
class VotingSystem:
    """A class to manage the ranking voting system."""

    _candidates: List[Candidate] = field(default_factory=list)
    _data: List[str] = field(init=False, compare=False, repr=False, default_factory=list)

    def __post_init__(self) -> None:
        self.generate_candidates_list()

    def generate_candidates_list(self) -> None:
        """Reads the candidates.csv file and creates a list of Candidate objects."""
        # Set the path to the candidates.csv file
        candidates_csv = Path(__file__).parent.parent / "data" / "candidates.csv"
        # Read the candidates.csv file
        with open(candidates_csv, "r") as data:
            # Create a CSV reader object
            reader = csv.reader(data)
            # Skip the header row
            next(reader)
            # Create a list of Candidate objects
            self._candidates = [
                Candidate(name=row[0], bio_url=row[1]) for row in reader
            ]

    def orcid_exists(self, orcid_id: str) -> bool:
        """Checks if an ORCID iD already exists in the database."""
        with session_scope() as session:
            try:
                return session.query(VoteModel.orcid_id).filter_by(orcid_id=orcid_id).first() is not None
            except Exception as e:
                raise DBException(f"An error occurred while checking if the ORCID iD exists: {e}")
            
    def record_vote_to_db(self, voter: Voter) -> None:
        """Adds a new entry to the votes table."""
        # Create a new entry in the votes table
        new_vote = VoteModel(
            full_name=voter.full_name,
            email=voter.email,
            orcid_id=voter.orcid_id,
            selection_1=voter.selection_1,
            selection_2=voter.selection_2,
            selection_3=voter.selection_3,
            selection_4=voter.selection_4,
            timestamp=voter.timestamp
        )
        
        # Add the new Vote instance to the database session and commit the changes
        with session_scope() as session:
            try:
                session.add(new_vote)
            except Exception as e:
                raise DBException(f"An error occurred while adding the new vote to the database: {e}")
            
    def record_vote(self, voter: Voter) -> None:
        """Creates a .csv file with the voter's selections, appends to the vote.log and prints the vote."""
        # Set the path to the new CSV file
        response_csv = Path(__file__).parent.parent / "data" / f"{voter.orcid_id}_{voter.timestamp}.csv"

        # Get the data format
        data = voter.prepare_data(self._candidates)
        
        # Write the data to the new CSV file
        with open(response_csv, "w") as file:
            writer = csv.writer(file)
            writer.writerow(["FullName", "Email", "ORCIDiD", "Pref1", "Pref2", "Pref3", "Pref4"])
            writer.writerow(data)

        # Append the vote to the log file
        vote_logger.info(f"New vote submited: {voter.full_name}, {voter.email}, {voter.orcid_id}, {[candidate.name for candidate in voter.selections_list]}, vote timestamp: {voter.timestamp}")
        
        # Print the vote
        print(f"New vote submited: {voter.full_name}, {voter.email}, {voter.orcid_id}, {[candidate.name for candidate in voter.selections_list]}, vote timestamp: {voter.timestamp}")
    
    @property
    def candidates(self) -> List[Candidate]:
        """Returns the list of candidates."""
        return self._candidates
