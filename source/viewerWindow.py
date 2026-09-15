# Handles the viewing window GUI

import dearpygui.dearpygui as dpg
import os
import shutil
import json
import math
from viewer import Viewer
from infoWindow import InfoWindow

class ViewerWindow:

    # Constructor
    def __init__(self, databaseHandler):

        # Config
        self.app_config = {
            
        }

        self.viewer = Viewer(databaseHandler)

        self.query_tags = []
        self.query_results = None
        self.viewer_page = 0
        self.viewer_page_start = 0
        self.viewer_page_end = 50

        self.query_image_button_memory = []

        self.test = 0

    # Creates the database window
    def create_window(self):

        # Handles what happens when you click a button
        def on_click_query_result_button(sender, app_data, user_data):

            entry = user_data

            infoWindow = InfoWindow(entry)
            infoWindow.create_window()

        # Displays the results of a query
        def display_query():

            # Creates table for results (if it does not exist already)
            if not (dpg.does_alias_exist("results_table")):
                with dpg.table(header_row = False, resizable = False, hideable = False, reorderable = False, borders_outerV = True, borders_innerH = True, tag = "results_table", parent = "results_subwindow"):
                    for i in range(0, 10, 1):
                        dpg.add_table_column(tag = "results_table_col_" + str(i))

            # Clears the previous search
            else:
                dpg.delete_item("results_table", children_only = True, slot = 1)

            display_page()
        
                

        # Displays a single page of the query results
        def display_page():

            result_counter = 0
            for row in range(math.floor(len(self.query_results) / 10) + 1):
                with dpg.table_row(tag = "results_table_row_" + str(row), parent = "results_table"):
                    for col in range(10):
                        if (result_counter < len(self.query_results)):
                            entry = self.query_results[result_counter]


                            # Loads image to dpg, if it does not already exist
                            if not (dpg.does_alias_exist(entry["album_name"] + "_thumbnail_texture")):
                                width, height, channels, data = dpg.load_image(entry["thumbnail_path"])
                                with dpg.texture_registry():
                                    dpg.add_static_texture(width = width, height = height, default_value = data, tag = entry["album_name"] + "_thumbnail_texture")
                
                            dpg.add_image_button(entry["album_name"] + "_thumbnail_texture", width = 90, height = 90, callback = on_click_query_result_button, user_data = entry, tag = entry["album_name"] + "_image_button")
                            self.query_image_button_memory.append(entry["album_name"] + "_image_button")
                            
                            result_counter += 1

        # Initiates a search with given criteria
        def query_databases():

            # Gets query results
            results = self.viewer.search_dbs(self.query_tags)
            self.query_results = results
            print("Query results completed. Number of results: " + str(len(results)))
            display_query()

        # Adds a tag to the query
        def add_tag_to_query():
            query_tag = dpg.get_value("input_tag_text")

            if not (query_tag in self.query_tags):
                self.query_tags.append(query_tag)
                dpg.add_button(label = query_tag, parent = "tag_list", tag = query_tag + "_button", callback = remove_tag_from_query, user_data = [query_tag + "_button", query_tag])

        # Removes a tag from query
        def remove_tag_from_query(sender, app_data, user_data):
            button_tag = user_data[0]
            query_tag = user_data[1]

            dpg.delete_item(button_tag)
            self.query_tags.remove(query_tag)

        # Removes all tags from the query
        def remove_all_tags_from_query():
            for query_tag in self.query_tags:
                try:
                    dpg.delete_item(query_tag + "_button")
                except:
                    pass

            self.query_tags = []

    
        # Starting window
        with dpg.window(label = "Viewer Window", width = 1050, height = 900, pos = (0, 0), tag = "vw_window"):

            with dpg.child_window(width = 1025, height = 800, menubar = True, resizable_x = True):

                # Menu Bar
                with dpg.menu_bar():
                    dpg.add_menu(label="Search Options")

                # Tag Filters
                with dpg.tree_node(label = "Tags"):
                    with dpg.child_window(autosize_x = True, height = 300):

                        # Submit new tags
                        with dpg.group(horizontal = True):
                            dpg.add_input_text(hint = "Input Tag Here", tag = "input_tag_text")
                            dpg.add_button(label = "Submit Tag", callback = add_tag_to_query)
                            dpg.add_button(label = "Clear All Tags", callback = remove_all_tags_from_query)

                        # Shows tags
                        with dpg.group(horizontal = False, tag = "tag_list"):
                            pass

                # Advanced Filters
                with dpg.tree_node(label = "Advanced"):
                    with dpg.child_window(autosize_x = True, height = 300):
                        with dpg.group(horizontal = True, width = 0):

                            # Database Filters
                            with dpg.child_window(width = 150, height = 300):
                                with dpg.tree_node(label = "Database 1"):
                                    dpg.add_button(label = "Include")
                                    dpg.add_button(label = "Exclude")
                                with dpg.tree_node(label = "Database 2"):
                                    dpg.add_button(label = "Include")
                                    dpg.add_button(label = "Exclude")
                                with dpg.tree_node(label = "Database 3"):
                                    dpg.add_button(label = "Include")
                                    dpg.add_button(label = "Exclude")

                            # Special Filters Results
                            with dpg.child_window(width = 300, height = 300):
                                dpg.add_button(label = "Button 1")
                                dpg.add_button(label = "Button 2")
                                dpg.add_button(label = "Button 3")

                            # Playlists (?)
                            with dpg.child_window(width = 50, height = 150):
                                dpg.add_button(label = "B1", width = 25, height = 25)
                                dpg.add_button(label = "B2", width = 25, height = 25)
                                dpg.add_button(label = "B3", width = 25, height = 25)

                # Search Results
                dpg.add_button(label = "Search", width = 1000, callback = query_databases)

                # Results navigation menu
                with dpg.group(width = 1000, tag = "results_navigation_group"):
                    with dpg.table(header_row = False, resizable = False, hideable = False, reorderable = False, borders_outerV = True, borders_innerH = True, policy = dpg.mvTable_SizingStretchSame, tag = "results_navigation_table"):
                        dpg.add_table_column(label="temp1")
                        dpg.add_table_column(label="temp2")

                        with dpg.table_row():
                            dpg.add_button(label = "Previous Page", width = -1)
                            dpg.add_button(label = "Next Page", width = -1)
                            
                        with dpg.table_row():
                            dpg.add_input_int(label = "test", width = -1)
                            dpg.add_button(label = "Test Button 3", width = -1)

                # Results subwindow
                with dpg.child_window(width = 1000, tag = "results_subwindow"):
                     pass
                    

    
    