# Handles the database window

import dearpygui.dearpygui as dpg
import os
import shutil
import json

class DatabaseWindow:

    # Constructor
    def __init__(self, databaseHandler):

        # Config
        self.app_config = {
            
        }


        self.dbh = databaseHandler
        self.combo_value = ""
        self.custom_tags = []

    # Creates the database window
    def create_window(self):

        # Parses the combo selection to pick which UI is used
        def parse_combo():
            combo_value = dpg.get_value("db_combo")

            # Does nothing if the current selection is chosen
            if (combo_value == self.combo_value):
                return

            # Unloads current UI
            try:
                dpg.delete_item("db_window_ui", children_only = True, slot = 1)
            except:
                pass

            # Loads new UI
            if (combo_value == "Add new database"):
                self.combo_value = combo_value
                load_db_creator_ui()

            else:
                self.combo_value = combo_value
                load_db_editor_ui()

        # Loads the UI for creating new databases
        def load_db_creator_ui():
            text = dpg.add_text(default_value = "Enter a name for a new database: ", tag = "db_name_text", parent = "db_window_ui")
            input_text = dpg.add_input_text(hint = "Enter database name", tag = "db_name_input", parent = "db_window_ui", width = 700)
            name_submit_button = dpg.add_button(label = "Add new database", tag = "db_name_submit_button", parent = "db_window_ui", callback = on_adding_new_database, user_data = [input_text])

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
            path_text = dpg.add_text(default_value = "Enter a database path below: ", tag = "db_path_text", parent = "db_window_ui")
            path_input_text = dpg.add_input_text(tag = "db_path_input", parent = "db_window_ui", width = 700)
            path_submit_button = dpg.add_button(label = "Submit database path", tag = "db_path_submit_button", callback = process_db_submission, user_data = [path_input_text, path_text], before = "db_reindex_button", parent = "db_window_ui", width = 500)
            force_reindex_button = dpg.add_button(label = "Force Re-Index Database", tag = "db_reindex_button", callback = on_reindex, user_data = [path_input_text, path_text], parent = "db_window_ui", width = 500)

            dpg.set_value(path_input_text, self.dbh.get_database_by_name(self.combo_value).get_database_path())

            # Custom Tags UI
            load_custom_tag_ui()
            

        # Lods the UI used for adding custom tags
        def load_custom_tag_ui():
            try:
                dpg.delete_item("custom_tag_ui_tree")
            except:
                pass

            with dpg.tree_node(label = "Custom Tags", parent = "db_window_ui", tag = "custom_tag_ui_tree", default_open = True):
                with dpg.child_window(width = 700):
                    with dpg.table(header_row = False, resizable = False, hideable = False, reorderable = False, borders_outerV = True, borders_innerH = True, policy = dpg.mvTable_SizingStretchSame, tag = "custom_tag_menu"):
                        dpg.add_table_column(label="temp1", init_width_or_weight = 400)
                        dpg.add_table_column(label="temp2", init_width_or_weight = 200)
                        dpg.add_table_column(label="temp2", init_width_or_weight = 100)

                        # Add custom tags to menu
                        custom_tag_info = self.dbh.get_database_by_name(self.combo_value).get_custom_special_tags()

                        for custom_tag in custom_tag_info.keys():
                            with dpg.table_row():
                                dpg.add_text(custom_tag)                            # Tag Name
                                dpg.add_text(custom_tag_info[custom_tag])           # Tag Type
                                dpg.add_button(label = "Delete", width = 100)

                        with dpg.table_row():
                            dpg.add_input_text(hint = "Custom Tag Name", tag = "custom_tag_input_text", width = 400)
                            dpg.add_combo(items = ["Integer", "String"], tag = "custom_tag_input_combo", width = 200)
                            dpg.add_button(label = "Add", tag = "custom_tag_add_button", callback = add_custom_tag, width = 100)

        # Adds a custom tag to a database
        def add_custom_tag():
            database = dpg.get_value("db_combo")
            custom_tag_name = dpg.get_value("custom_tag_input_text")
            custom_tag_combo = dpg.get_value("custom_tag_input_combo")

            # Determines default value by the combo
            default_value = 0
            if (custom_tag_combo == "Integer"):
                default_value = 0

            elif (custom_tag_combo == "String"):
                default_value = ""

            # Adds to database
            self.dbh.add_custom_tag_to_database(database, [custom_tag_name], [default_value], [custom_tag_combo])

            # Reloads custom tag ui
            load_custom_tag_ui()
            

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
                dpg.set_value("db_path_text", "Database Initialization Successful")

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
        with dpg.window(label = "Database Window", width = 825, height = 600, pos = (1050, 0), tag = "db_window"):

            # Database Picker
            combo_options = self.dbh.get_database_names()
            combo_options.insert(0, "Add new database")
            database_combo = dpg.add_combo(combo_options, height_mode = dpg.mvComboHeight_Regular, tag = "db_combo", callback = parse_combo)
            dpg.set_value(database_combo, "Add new database")
            self.combo_value = "Add new database"

            # Start on the database creator
            with dpg.child_window(tag = "db_window_ui", width = 800, height = 500, menubar = False):
                pass

            load_db_creator_ui()

            
            

    
    

