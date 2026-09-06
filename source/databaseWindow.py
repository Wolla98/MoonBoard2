# Handles the database window

import dearpygui.dearpygui as dpg
import os
import shutil
import json
from database import Database

class DatabaseWindow:

    # Constructor
    def __init__(self, databaseHandler):

        # Config
        self.app_config = {
            
        }


        self.dbh = databaseHandler
        self.combo_value = ""

    # Creates the database window
    def create_window(self):

        # Parses the combo selection to pick which UI is used
        def parse_combo():
            combo_value = dpg.get_value("db_combo")

            # Does nothing if the current selection is chosen
            if (combo_value == self.combo_value):
                return

            # Unloads current UI
            if (self.combo_value == "Add new database"):
                unload_db_creator_ui()

            else:
                unload_db_editor_ui()

            # Loads new UI
            if (combo_value == "Add new database"):
                self.combo_value = combo_value
                load_db_creator_ui()

            else:
                self.combo_value = combo_value
                load_db_editor_ui()

        # Loads the UI for creating new databases
        def load_db_creator_ui():
            text = dpg.add_text(default_value = "Enter a name for a new database: ", tag = "db_name_text", parent = "db_window")
            input_text = dpg.add_input_text(tag = "db_name_input", parent = "db_window")
            name_submit_button = dpg.add_button(label = "Add new database", tag = "db_name_submit_button", parent = "db_window", callback = on_adding_new_database, user_data = [input_text])

        # Unloads the UI for creating new databases
        def unload_db_creator_ui():
            unloaded_items = ["db_name_text", "db_name_input", "db_name_submit_button"]
            for item in unloaded_items:
                try:
                    dpg.delete_item(item)
                except:
                    pass

        # Runs when adding a new database
        def on_adding_new_database():

            # Checks that the name is not already an existing database
            new_db_name = dpg.get_value("db_name_input")
            combo_options = self.dbh.get_database_names()
            combo_options.insert(0, "Add new database")

            if (new_db_name in combo_options):
                dpg.set_value("db_name_text", "Database already exists. Enter a different name.")
                return

            # Add new name to databases
            self.dbh.create_database(new_db_name)
            combo_options = self.dbh.get_database_names()
            combo_options.insert(0, "Add new database")            

            # Updates combo with new item
            dpg.configure_item("db_combo", items = combo_options)
            dpg.set_value("db_combo", new_db_name)
            parse_combo() 

        # Loads the UI for modifying databases
        def load_db_editor_ui():

            # Adds UI Buttons
            path_text = dpg.add_text(default_value = "Enter a database path below: ", tag = "db_path_text", parent = "db_window")
            path_input_text = dpg.add_input_text(tag = "db_path_input", parent = "db_window")
<<<<<<< HEAD
            path_submit_button = dpg.add_button(label = "Submit database path", tag = "db_path_submit_button", callback = process_db_submission, user_data = [path_input_text, path_text], before = "db_reindex_button", parent = "db_window")
            force_reindex_button = dpg.add_button(label = "Force Re-Index Database", tag = "db_reindex_button", callback = on_reindex, user_data = [path_input_text, path_text], parent = "db_window")
=======
            path_submit_button = dpg.add_button(label = "Submit database path", tag = "db_path_submit_button", callback = process_db_submission, user_data = [path_input_text], before = "db_reindex_button", parent = "db_window")
>>>>>>> b8ffe9f667a9458d0fd66f83e5c76701fe23e41b

            dpg.set_value(path_input_text, self.dbh.get_database_by_name(self.combo_value).get_database_path())
            

        # Unloads the UI for modifying databases
        def unload_db_editor_ui():
            unloaded_items = ["db_path_text", "db_path_input", "db_path_submit_button", "db_reindex_button"]
            for item in unloaded_items:
                try:
                    dpg.delete_item(item)
                except:
                    pass

        # Process database path submission
        def process_db_submission(sender, app_data, user_data):

            input_text = user_data[0]

            # Attempts to read any existing JSON files
            db_name = self.combo_value
            db_path = dpg.get_value(input_text)
            result = self.dbh.on_new_database_submission(db_name, db_path)

            # Read Success
            if (result == 0):
                dpg.set_value("db_path_text", "Database JSON file found. Loaded sucessfully.")

            # Index Success
            elif (result == 1):
<<<<<<< HEAD
                dpg.set_value(text, "Database initialization successful.")
=======
                dpg.set_value("db_path_text", "Database Initialization Successful")
>>>>>>> b8ffe9f667a9458d0fd66f83e5c76701fe23e41b

            # Failure
            else:
                dpg.set_value("db_path_text", "ERROR [1]: Path does not exist.")

        # Runs when re-indexing a database
        def on_reindex(sender, app_data, user_data):

            input_text = user_data[0]
            text = user_data[1]

            # Attempts re-index
            db_name = self.combo_value
            db_path = dpg.get_value(input_text)
            result = self.dbh.reindex_database(db_name, db_path)

            if (result == 0):
                dpg.set_value(text, "Database re-index successful.")

            elif (result == 2):
                dpg.set_value(text, "Failure during database re-indexing.")

        

    
        # Starting window
        with dpg.window(label = "Database Window", width = 800, height = 600, pos = (0, 0), tag = "db_window"):

            # Database Picker
            combo_options = self.dbh.get_database_names()
            combo_options.insert(0, "Add new database")
            database_combo = dpg.add_combo(combo_options, height_mode = dpg.mvComboHeight_Regular, tag = "db_combo", callback = parse_combo)
            dpg.set_value(database_combo, "Add new database")
            self.combo_value = "Add new database"

            # Start on the database creator
            load_db_creator_ui()

            
            

    
    

