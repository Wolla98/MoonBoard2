# Handles the info panel window for individual entries

import dearpygui.dearpygui as dpg
import os
import shutil
import json
import math
import numpy as np

class InfoWindow:

    # Constructor
    def __init__(self, info, databasehandler):

        # Config
        self.app_config = {
            
        }

        self.info = info
        self.dbh = databasehandler
        self.window_name = "info_window_" + str(self.info["id"])

    
    # Creates the database window
    def create_window(self):

        # Clears the right window
        def clear_right_window():
            try:
                dpg.delete_item(self.window_name + "_song_info_panel", children_only = True, slot = 1)
            except:
                pass

        # Populates the right window with songs
        def show_songs():
            clear_right_window()

            for song in self.info["songs"]:
                button_text = song["song_name"] + "\n" + "Track Length: " + str(song["track_length"]) + "\n" + "Last Played: " + str(song["last_played"]) + "\n" + "Custom Tags: " + str(song["custom_special_tags"])
                dpg.add_button(width = 0, label = button_text, parent = self.window_name + "_song_info_panel", callback = show_song_info, user_data = song["song_id"])

        # Populates the right window with a singular song's info
        def show_song_info(sender, app_data, user_data):

            song_id = user_data
            song_info = self.info["songs"][song_id]

            clear_right_window()

            with dpg.child_window(width = 675, autosize_y = True, menubar = False, border = True, tag = self.window_name + "_song_info_subwindow", parent = self.window_name + "_song_info_panel"): 
                dpg.add_button(width = 0, label = "Return", callback = show_songs)
                dpg.add_text(song_info["song_name"])

                # More Info
                with dpg.tree_node(label = "More Info"):
                    pass

                # Custom Special Tags
                with dpg.tree_node(label = "Custom Special Tags"):
                    with dpg.table(header_row = False, resizable = False, hideable = False, reorderable = False, borders_outerV = True, borders_innerH = True, width = 625):
                        dpg.add_table_column(width_fixed = False)
                        dpg.add_table_column(width_fixed = False)

                        for custom_special_tag in song_info["custom_special_tags"].keys():
                            with dpg.table_row():
                                dpg.add_text(custom_special_tag)
                                dpg.add_text(str(song_info["custom_special_tags"][custom_special_tag]))

                # Custom Tags
                with dpg.tree_node(label = "Tags"):
                    pass

                # Player Info
                with dpg.tree_node(label = "Player Info", default_open = True):
                    dpg.add_button(label = "Open File", width = 625, callback = open_song_file, user_data = song_id)
                    dpg.add_button(label = "Get Track Length and Generate Waveform", width = 625, callback = load_song_for_info, user_data = song_info)

                    if len(song_info["waveform_data"]) > 0:
                        with dpg.child_window(tag = self.window_name + "_waveform_window", width = 650, height = 200, border = True, horizontal_scrollbar = True):

                            BARS = 100
                            BAR_HEIGHT = 100
                            LINE_WIDTH = 5
                            COLOR_1 = (255, 255, 255)
                            COLOR_2 = (255, 0, 255)
                            COLOR_3 = (128, 255, 0)

                            with dpg.drawlist(width = math.ceil(len(song_info["waveform_data"]) * LINE_WIDTH + 20), height = 200):

                                draw_x = 0
                                draw_y = 100

                                np_waveform_info = np.array(song_info["waveform_data"])
                                np_max = np.max(np_waveform_info)
                                np_min = np.min(np_waveform_info)
                            
                                normal_waveform = (np_waveform_info - np_min) / (np_max - np_min)
                                step = math.floor(len(normal_waveform) / BARS)

                                wave_counter = 1
                                for wave_data in normal_waveform:

                                    if (wave_counter % 12 == 0):
                                        dpg.draw_rectangle([draw_x, draw_y], [draw_x + LINE_WIDTH, draw_y + (BAR_HEIGHT * wave_data)], thickness = 0, color = COLOR_2, fill = COLOR_2)
                                        dpg.draw_rectangle([draw_x, draw_y], [draw_x + LINE_WIDTH, draw_y - (BAR_HEIGHT * wave_data)], thickness = 0, color = COLOR_2, fill = COLOR_2)

                                    else:
                                        dpg.draw_rectangle([draw_x, draw_y], [draw_x + LINE_WIDTH, draw_y + (BAR_HEIGHT * wave_data)], thickness = 0, color = COLOR_1, fill = COLOR_1)
                                        dpg.draw_rectangle([draw_x, draw_y], [draw_x + LINE_WIDTH, draw_y - (BAR_HEIGHT * wave_data)], thickness = 0, color = COLOR_1, fill = COLOR_1)

                                    draw_x = draw_x + (LINE_WIDTH)
                                    wave_counter += 1


        # Small helper function, converts seconds to a time string
        def seconds_to_string(seconds):
            remainder = seconds
            hours = math.floor(seconds / 3600)
            remainder = remainder - (hours * 3600)

            minutes = math.floor(seconds / 60)
            remainder = remainder - (minutes * 60)

            if (hours <= 0):
                return str(minutes) + " : " + str(seconds)

            else:
                return str(hours) + " : " + str(minutes) + " : " + str(seconds)

        # Opens a song file
        def open_song_file(sender, app_data, user_data):
            song_id = user_data
            os.startfile(self.info["songs"][song_id]["song_path"])

        # Loads the song for track length / waveform information
        def load_song_for_info(sender, app_data, user_data):
            song_info = user_data
            self.dbh.load_track_information(self.info["database_name"], self.info["id"], song_info["song_id"])
            self.info = self.dbh.get_database_by_name(self.info["database_name"]).data[self.info["id"]]
            show_song_info(sender, app_data, song_info["song_id"])
            

        # Starting window
        with dpg.window(label = str(self.info["album_name"]), width = 1525, height = 850, pos = (100, 100), tag = self.window_name):
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
                    with dpg.child_window(width = 700, height = 800, menubar = True, resizable_x = True, horizontal_scrollbar = True, tag = self.window_name + "_song_info_panel"):
                        pass

                    show_songs()