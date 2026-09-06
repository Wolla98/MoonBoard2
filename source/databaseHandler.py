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
            "json_path": ".\\data\\db_info.json",
            "data_folder": ".\\data"
        }

        # Data
        self.databases = []

        # Reads JSON to populate database information
        self.read_dbh_json()

    
    # Reads JSON file to get information about databases
    def read_dbh_json(self):

        # Creates an empty json if it doesn't exist
        if (os.path.exists(self.config["json_path"])):
            with open(os.path.join(self.config["json_path"]), "r") as f:
                json_data = json.load(f)

                for db_entry in json_data:
                    db = Database()
                    db.set_name(db_entry["name"])
                    db.read_db_from_json_path(db_entry["json_path"])

                    self.databases.append(db)


    # Handles new database submission
    def on_new_database_submission(self, db_name, db_path):

        # Attempts JSON read
        database = self.get_database_by_name(db_name)
        result1 = database.read_db_from_db_path(db_path)

        # Success
        if (result1 == 0):
            self.save_database_info()
            return 0

        # Read failure, attempts to index the database
        elif (result1 == 1):
            result2 = database.db_index_audio(db_path)

            # Success
            if (result2 == 0):
                database.save_db_to_json()
                self.save_database_info()
                return 1

            # Failure
            else:
                return 2

    # Handles re-indexing a database
    def reindex_database(self, db_name, db_path):
        db = self.get_database_by_name(db_name)
        result = db.db_index_audio(db_path)
        if (result == 0):
            return 0
        
        else:
            return 2

    # Saves database information to a local json
    def save_database_info(self):

        # Save Data
        data = []
        for db in self.databases:
            db_info = {
                "name": db.get_name(),
                "path": db.get_database_path(),
                "json_path": db.get_json_path()
            }

            data.append(db_info)

        # Write to JSON
        os.makedirs(self.config["data_folder"], exist_ok = True)
        with open(self.config["json_path"], "w") as f:
            json.dump(data, f, indent = 2)


    # Creates a new database with a given name
    def create_database(self, name):
        new_database = Database()
        new_database.metadata["database_name"] = name

        self.databases.append(new_database)
        self.save_database_info()
        return new_database


    # Returns the list of database names
    def get_database_names(self):
        names = []

        for database in self.databases:
            names.append(database.metadata["database_name"])

        return names

    # Returns a database by name
    def get_database_by_name(self, name):
        for db in self.databases:
            if db.get_name() == name:
                return db


    # Initiates a search of each database and returns the results
    def search_dbs(self, tags):
        results = []
        for db in self.databases:
            db_search_results = db.search_db(tags)

            for search_result in db_search_results:
                results.append(search_result)

        return results