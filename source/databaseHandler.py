# Handles functions related to storing / using multiple databases

import os
import json
import datetime
from database import Database

class DatabaseHandler:

    # Constructor
    def __init__(self):

        # Config
        self.config = {
        }

        # Data
        self.databases = []

    # Creates a new database with a given name
    def create_database(self, name):
        new_database = Database()
        new_database.metadata["database_name"] = name

        self.databases.append(new_database)


    # Returns the list of database names
    def get_database_names(self):
        names = []

        for database in self.databases:
            names.append(database.metadata["database_name"])

        return names