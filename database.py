import json, sys

class AegisDB:

    def __init__(self, db_file):
        self.db_file = db_file
        self.database = {}
        self.current_backup = 0
        self.initialize()

    def initialize(self):
        try:
            self.load()
        except Exception as err:
            print(f"[AegisDB] Couldn't load database, starting fresh! Error: {err}")
            self.database = {"files": {}, "backups": []}

    def load(self):
        try:
            with open(self.db_file, "r+") as file:
                self.database = json.load(file)
            print(f"[AegisDB] Successfully loaded {self.db_file}")
        except:
            raise # unsure where to handle DB loading errors; letting initialize error out currently
        
    def save(self):
        try:
            with open(self.db_file, "w+") as file:
                json.dump(self.database, file, indent=4, sort_keys=True)
        except Exception as err:
            print(f"[AegisDB] Failed to save database on quit. There may be missing data on next start. Err: {err}")
            print(self.database)

    def get(self):
        return self.database
    
    # insert into the database a latest snapshot record for a particular file
    def update_file(self, filename, hash):
        self.database["files"][filename]["backups"][self.current_backup] = hash
        self.database["files"][filename]["last_changed"] = (self.current_backup, hash)

    # create a new file entry into the database
    def create_file(self, filename, hash):
        self.database["files"][filename] = {"last_changed": (), "backups":{}}
        self.database["files"][filename]["backups"][self.current_backup] = hash
        self.database["files"][filename]["last_changed"] = (self.current_backup, hash)

    # return a boolean for whether or not a file already exists in the database
    def file_exists(self, filename):
        if filename in self.database["files"]:
            return True
        return False

    # gets the latest time when a snapshot was taken
    def get_latest_backup(self):
        self.database["backups"].sort() # get the last as that'll be the highest epoch count; meaning it's the newest
        return self.database["backups"][-1]

    # record when we're taking a snapshot
    def record_backup(self, timestamp):
        self.current_backup = str(timestamp)

    # save the backup timestamp when everything is successful.
    def commit_backup(self):
        self.database["backups"].insert(0, str(self.current_backup))

    # returns a tuple containing the latest hash and timestamp of when a file was backed up.
    def get_latest_file_hash(self, filename):
       # latest_backup = self.get_latest_backup()
        return self.database["files"][filename]["last_changed"][1]

    def get_latest_file_timestamp(self, filename):
        return self.database["files"][filename]["last_changed"][0]
    