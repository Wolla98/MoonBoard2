import dearpygui.dearpygui as dpg
from databaseWindow import DatabaseWindow
from viewerWindow import ViewerWindow
from databaseHandler import DatabaseHandler

def save_callback():
    print("Save Clicked")


# Boot sequence
def boot():

    # Windows
    database_handler = DatabaseHandler()
    dbw = DatabaseWindow(database_handler)
    vww = ViewerWindow(database_handler)

    # Create viewport
    dpg.create_context()
    dpg.create_viewport(title='Custom Title', width = 1920, height = 1080)



    # Test
    dbw.create_window()
    vww.create_window()


    # Run
    # dpg.show_item_registry()
    
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()

boot()