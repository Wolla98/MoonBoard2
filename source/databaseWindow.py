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

        # # Initializes database on startup
        # def process_db_submission(sender, app_data, user_data):

        #     input_text = user_data[0]
        #     text = user_data[1]
        #     reindex_button = user_data[2]

        #     # Attempts to read any existing JSON files
        #     db_path = dpg.get_value(input_text)
        #     result1 = self.db_data.read_db_from_db_path(db_path)

        #     # Success
        #     if (result1 == 0):
        #         dpg.set_value(text, "Database JSON file found. Loaded sucessfully.")
        #         dpg.show_item(reindex_button)

        #     # Read Failure
        #     elif (result1 == 1):
        #         dpg.set_value(text, "ERROR [2]: Archive JSON file exists, but failed to read.")
        #         return False

        #     # If a database JSON does not already exists, then indexes the database to create a new one
        #     elif (result1 == 2):
        #         result = self.db_data.db_index_audio(db_path)

        #         if (result == 0):
        #             self.db_data.save_db_to_json()
        #             dpg.set_value(text, "Database Initialization Successful")
        #             dpg.show_item(reindex_button)
                  
        #         elif (result == 1):
        #             dpg.set_value(text, "ERROR [1]: Path does not exist.")


        # # Re-indexes database
        # def reindex_db(sender, app_data, user_data):
        #     text = user_data

        #     result = self.db_data.db_index_audio()
            
        #     if (result == 0):
        #         dpg.set_value(text, "Database Initialization Successful")
        #         dpg.show_item(reindex_button)
                
        #     elif (result == 1):
        #         dpg.set_value(text, "ERROR [1]: Path does not exist.")
        

        # Parses the combo selection to pick which UI is used
        def parse_combo():
            combo_value = dpg.get_value("db_combo")

            # Does nothing if the current selection is chosen
            if (combo_value == self.combo_value):
                return

            if (combo_value == "Add new database"):
                self.combo_value = combo_value
                unload_db_editor_ui()
                load_db_creator_ui()

            else:
                self.combo_value = combo_value
                unload_db_creator_ui()
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
                dpg.delete_item(item)

        # Runs when adding a new database
        def on_adding_new_database():

            # Checks that the name is not already an existing database
            new_db_name = dpg.get_value("db_name_input")
            combo_options = self.dbh.get_database_names()
            combo_options.insert(0, "Add new database")

            if (new_db_name in combo_options):
                dpg.set_value("db_status_text", "Database already exists. Enter a different name.")
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
            pass

        # Unloads the UI for modifying databases
        def unload_db_editor_ui():
            pass

    
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

            # reindex_button = dpg.add_button(label = "Re-index Database", tag = "db_reindex_button", callback = reindex_db, user_data = text, show = False)
            # path_submit_button = dpg.add_button(label = "Submit", tag = "db_path_submit_button", callback = process_db_submission, user_data = [input_text, text, reindex_button], before = "db_reindex_button")
            

    
    

