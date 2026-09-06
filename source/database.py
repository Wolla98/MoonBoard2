# Handles functions related to database and data handling

import os
import json
import datetime
from PIL import ImageTk, Image

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
            "thumbnail_path": "",
            "last_time_indexed": -1,
        }
        self.data = {}

    # Indexes a database to memory
    # Specifically for audio
    # Returns 0 if successful, 1 if the input path does not exist
    def db_index_audio(self, db_path = None):

        if not (os.path.exists(db_path)):
            return 1

        # By default, uses the database path stored in memory
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

            # Ignores thubmnails
            if (folder == "thumbnails"):
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
        self.metadata["thumbnail_path"] = os.path.join(db_path, "thumbnails")

        dt = datetime.datetime.now()
        self.metadata["last_time_indexed"] = dt.timestamp()
        self.data = db_entries

        self.save_db_to_json()
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
            with open(os.path.join(db_path, self.config["default_json_name"]), "r") as f:
                json_data = json.load(f)

                self.metadata = json_data["db_metadata"]
                self.data = json_data["db_data"]

            return 0

        except:
            return 1

    # Reads stored data from a json path
    # Returns 0 if successful, 1 if exists but unsuccessful, and 2 if it the file does not exist
    def read_db_from_json_path(self, json_path):
    
        # Checks that the file exists
        if not (os.path.isfile(json_path)):
            return 2

        try:
            with open(json_path, "r") as f:
                json_data = json.load(f)

                self.metadata = json_data["db_metadata"]
                self.data = json_data["db_data"]

            return 0

        except:
            return 1


    # Searches the database for all entries that match a specific search criteria
    # Right now, only searches using tags and name

    # Searches the following criteria:
    # In album information: album name, voice artist, cover artist, circle
    # In song information, song name, custom special tags, custom tags, and user notes
    def search_db(self, tags):
        return_list = []
        thumbnail_created = False

        for entry in self.data:

            accept_flag = True
            for tag in tags:

                # Checks album information first
                if (tag in entry["album_name"]) or (tag in entry["voice_artist"]) or (tag in entry["cover_artist"]) or (tag in entry["circle"]):
                    continue

                # Checks each song
                song_flag = False
                for song in entry["songs"]:

                    if (tag in song["song_name"]) or (tag in song["user_notes"]):
                        song_flag = True

                    for custom_special_tag in song["custom_special_tags"]:
                        if tag in custom_special_tag:
                            song_flag = True

                    for custom_tag in song["custom_tags"]:
                        if tag in custom_tag:
                            song_flag = True

                if (song_flag):
                    continue

                # If no conditions were passed, then fails the criteria
                accept_flag = False
                continue

            # If the entry passes all criteria, then accepts it
            if (accept_flag):

                # Checks that each result has a thumbnail before accepting
                entry_thumbnail_path = entry["thumbnail_path"]
    
                # Creates a thumbnail if it does not already exist
                if not (os.path.exists(entry_thumbnail_path)):
                    os.makedirs(os.path.join(self.metadata["thumbnail_path"]), exist_ok = True)
    
                    # Shrinks cover image to thumbnail path
                    new_thumbnail_path = os.path.join(self.metadata["thumbnail_path"], entry["album_name"] + "_thumbnail.png")

                    try:
                        cover_image = Image.open(entry["cover_image_path"])
                        cover_image = cover_image.resize((150, 150))
                        cover_image.save(new_thumbnail_path)

                        entry["thumbnail_path"] = new_thumbnail_path
                        thumbnail_created = True
                        print("Thumbnail image creation succeeded for: " + str(entry["album_name"]))

                    except:
                        print("Thumbnail image creation failed for: " + str(entry["album_name"]))
                        return_list.append(entry)
                        continue

            return_list.append(entry)

        # If any thumbnails were created, saves changes to the JSON file
        self.save_db_to_json()

        return return_list

        

    # -----------------------
    def get_name(self):
        return self.metadata["database_name"]

    def get_database_path(self):
        return self.metadata["database_path"]

    def get_json_path(self):
        return self.metadata["json_path"]


    def set_name(self, name):
        self.metadata["database_name"] = name