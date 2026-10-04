# Holds app configuration data
# Mostly GUI data

import math

class AppConfig:

    def __init__(self, width, height, window_padding_horizontal, window_padding_vertical, internal_padding_horizontal, internal_padding_vertical):

        self.width = width                                              # Window width, in pixels
        self.height = height                                            # Window height, in pixels
        self.window_padding_horizontal = window_padding_horizontal      # Padding between internal UI windows and the border of the app's window, in pixels
        self.window_padding_vertical = window_padding_vertical          #
        self.internal_padding_horizontal = internal_padding_horizontal  # Padding between UI elements within windows and the border of internal UI windows, in pixels
        self.internal_padding_vertical = internal_padding_vertical      #



    # Calculates a given size for an object given a percent size of a window's size
    # Width
    def calc_ww(self, percent_size):
        return math.floor(self.width * percent_size)

    def calc_iw(self, percent_size, width):
        return math.floor(width * percent_size)

    # Height
    def calc_wh(self, percent_size):
        return math.floor(self.height * percent_size)

    def calc_ih(self, percent_size, height):
        return math.floor(height * percent_size)


    # Get 
    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def get_wph(self):
        return self.window_padding_horizontal

    def get_wpv(self):
        return self.window_padding_vertical

    def get_iph(self):
        return self.internal_padding_horizontal

    def get_ipv(self):
        return self.internal_padding_vertical


    # Set
    def set_width(self, width):
        self.width = width

    def set_height(self, height):
        self.height = height

    def set_wph(self, window_padding_horizontal):
        self.window_padding_horizontal = window_padding_horizontal

    def set_wpv(self, window_padding_vertical):
        self.window_padding_vertical = window_padding_vertical

    def set_iph(self, internal_padding_horizontal):
        self.internal_padding_horizontal = internal_padding_horizontal

    def set_ipv(self, internal_padding_vertical):
        self.internal_padding_vertical = internal_padding_vertical