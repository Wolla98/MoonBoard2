import dearpygui.dearpygui as dpg
from databaseWindow import DatabaseWindow
from viewerWindow import ViewerWindow
from databaseHandler import DatabaseHandler
import os

def save_callback():
    print("Save Clicked")


# Boot sequence
def boot():
    dpg.create_context()

    # Register font
    with dpg.font_registry():
        en_font_path = ".\\assets\\fonts\\NotoSerif.ttf"
        jp_font_path = ".\\assets\\fonts\\NotoSerifJP.ttf"
        default_font = dpg.add_font(jp_font_path, size = 20, tag = "default_font")
    dpg.bind_font(default_font)

    # Windows
    database_handler = DatabaseHandler()
    dbw = DatabaseWindow(database_handler)
    vww = ViewerWindow(database_handler)

    # Create viewport
    dpg.create_viewport(title='Custom Title', width = 1920, height = 1080)


    # Create windows
    dbw.create_window()
    vww.create_window()


    # Run
    dpg.show_item_registry()
    
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()

boot()