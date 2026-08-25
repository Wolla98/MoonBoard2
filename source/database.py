# Handles functions related to database and data handling

import os
import json
import datetime

class Database:

    # Constructor
    def __init__(self):

        # Config
        self.config = {
            "default_json_name": "db_archive.json"
        }

        # Data
        self.metadata = {
            "database_name": "",
            "database_path": "",
            "json_path": "",
            "last_time_indexed": -1,
        }
        self.data = {}

    # Indexes a database to memory
    # Specifically for audio
    # Returns 0 if successful, 1 if the input path does not exist
    def db_index_audio(self, db_path = None):

        if not (os.path.exists(db_path)):
            return 1

        # By default, uses the databae path stored in memory
        if (db_path == None):
            db_path = self.metadata["database_path"]

        # File whitelist
        song_ext_whitelist = [".mp3", ".MP3", ".wav", ".flac"]
        cover_ext_whitelist = [".jpg", ".jpeg", ".webp", ".png"]

        db_entries = []
        counter = 0

        folders = os.listdir(db_path)
        folders.sort()

        # Albums
        for folder in folders:
            folder_path = os.path.join(db_path, folder)

            # Ignores files
            if (os.path.isfile(folder_path)):
                continue

            files = os.listdir(folder_path)
            files.sort()

            # Adds album information
            entry = {
                "id": counter,
                "album_name": folder,
                "voice_artist": "",
                "cover_artist": "",
                "circle": "",
                "album_path": folder_path,
                "thumbnail_path": "",
                "cover_image_path": "",
                "songs": []
            }

            song_counter = 0

            # Individual songs
            for file in files:
                file_name, ext = os.path.splitext(file)

                # Songs
                if (ext in song_ext_whitelist):
                    song_info = {
                        "song_id": song_counter,
                        "song_name": file_name,
                        "song_path": os.path.join(folder_path, file),
                        "track_number": -1,
                        "track_length": -1,
                        "custom_special_tags": {},
                        "custom_tags": [],
                        "last_played": -1,
                        "play_log": [],
                        "times_played": 0,
                        "user_notes": "",
                    }

                    entry["songs"].append(song_info)
                    song_counter += 1

                # Cover Image
                elif (ext in cover_ext_whitelist):
                    entry["cover_image_path"] = os.path.join(folder_path, file)


            # Adds the entry to the database
            db_entries.append(entry)
            counter += 1

        # Saves data to memory
        self.metadata["database_path"] = db_path
        self.metadata["json_path"] = os.path.join(db_path, self.config["default_json_name"])

        dt = datetime.datetime.now()
        self.metadata["last_time_indexed"] = dt.timestamp()
        self.data = db_entries
        return 0


    # Saves stored data to JSON
    def save_db_to_json(self):
        with open(self.metadata["json_path"], "w") as f:
            temp = {
                "db_metadata": self.metadata,
                "db_data": self.data
            }

            json.dump(temp, f, indent = 2)

    # Reads stored data from database path (using default json name)
    # Returns 0 if successful, 1 if exists but unsuccessful, and 2 if it the file does not exist
    def read_db_from_db_path(self, db_path):

        # Checks that the file exists
        if not (os.path.isfile(os.path.join(db_path, self.config["default_json_name"]))):
            return 2

        try:
            print(os.path.join(db_path, self.config["default_json_name"]))
            with open(os.path.join(db_path, self.config["default_json_name"]), "r") as f:
                json_data = json.load(f)

                print("flag1")
                self.metadata = json_data["db_metadata"]
                self.data = json_data["db_data"]
                print("flag2")

            return 0

        except:
            return 1