# Handles the info panel window for individual entries

import dearpygui.dearpygui as dpg
import os
import shutil
import json
import math

class InfoWindow:

    # Constructor
    def __init__(self, info):

        # Config
        self.app_config = {
            
        }

        self.info = info
        self.window_name = "info_window_" + str(self.info["id"])

    
    # Creates the database window
    def create_window(self):

        with dpg.window(label = "Info Window", width = 1525, height = 850, pos = (100, 100)):
            with dpg.table(header_row = False, resizable = False, hideable = False, reorderable = False, borders_outerV = True, borders_innerH = True, width = 1500):

                # Creates divider dimensions
                dpg.add_table_column(width_fixed = True, init_width_or_weight = 800)
                dpg.add_table_column(width_fixed = True, init_width_or_weight = 700)

                with dpg.table_row():

                    # Adds image on the left side
                    with dpg.child_window(width = 800, height = 800, menubar = True, resizable_x = True):
                                                    
                        # Loads image to dpg, if it does not already exist
                        if not (dpg.does_alias_exist(self.info["album_name"] + "_cover_image_texture")):

                            try:
                                width, height, channels, data = dpg.load_image(self.info["cover_image_path"])
                                with dpg.texture_registry():
                                    dpg.add_static_texture(width = width, height = height, default_value = data, tag = self.info["album_name"] + "_cover_image_texture")
                                dpg.add_image(self.info["album_name"] + "_cover_image_texture", width = 800, height = (800 / width) * height)
                                
                            except:
                                dpg.add_text("Failed to load image")

                        else:
                            with dpg.texture_registry():
                                width = dpg.get_item_width(self.info["album_name"] + "_cover_image_texture")
                                height = dpg.get_item_height(self.info["album_name"] + "_cover_image_texture")
                            dpg.add_image(self.info["album_name"] + "_cover_image_texture", width = 800, height = (800 / width) * height)

                    # Adds buttons on the right
                    with dpg.child_window(width = 700, height = 800, menubar = True, resizable_x = True, horizontal_scrollbar = True):
                        for song in self.info["songs"]:
                            button_text = song["song_name"] + "\n" + "Track Length: " + str(song["track_length"]) + "\n" + "Last Played: " + str(song["last_played"]) + "\n" + "Custom Tags: " + str(song["custom_tags"])
                            dpg.add_button(width = 0, label = button_text)