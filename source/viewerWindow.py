# Handles the viewing

import dearpygui.dearpygui as dpg
import os
import shutil
import json

class ViewerWindow:

    # Constructor
    def __init__(self, databaseHandler):

        # Config
        self.app_config = {
            
        }

        self.dbh = databaseHandler

    # Creates the database window
    def create_window(self):
    
        # Starting window
        with dpg.window(label = "Viewer Window", width = 1100, height = 900, pos = (800, 0), tag = "vw_window"):

            with dpg.child_window(width = 1000, height = 800, menubar = True):

                # Menu Bar
                with dpg.menu_bar():
                    dpg.add_menu(label="Search Options")

                # Tag Filters
                with dpg.tree_node(label = "Tags"):
                    with dpg.child_window(autosize_x = True, height = 300):
                        with dpg.group(horizontal=True):
                            dpg.add_button(label = "Tag 1", width = 75, height = 75)
                            dpg.add_button(label = "Tag 2", width = 75, height = 75)
                            dpg.add_button(label = "Tag 3", width = 75, height = 75)

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
                with dpg.group(horizontal = True, width = 1000):
                    dpg.add_button(label="Search", width=175)
                    dpg.add_text("Footer 2")

    
    