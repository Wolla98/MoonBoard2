# Handles functions related to viewing / searching multiple databases

import os
import json
import datetime
from databaseHandler import DatabaseHandler

class Viewer():
    
    # Constructor
    def __init__(self, dbHandler):

        # Config
        self.config = {

        }

        self.dbh = dbHandler

    # Initiates a search on the databases given some search criteria
    def search_dbs(self, tags):

        result = self.dbh.search_dbs(tags)
        return result