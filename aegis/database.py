import json, logging, errno

class Database:

    def __init__(self, config):
        self.logger = logging.getLogger("AegisDB")
        self.db_file = config["database_path"]
        self.database = {}
        self.current_backup = 0
        self.initialize()

    def initialize(self):
        try:
            self.load()
        except OSError as err:
            if err.errno == errno.ENOENT:
                self.logger.info(f"Aegis database doesn't exist at {self.db_file}, creating now.")
                self.new_database()
            elif err.errno == errno.EACCES:
                self.logger.error(f"Permission denied when accessing Aegis database at {self.db_file}. Error: {err}")
                raise
        except json.JSONDecodeError as err:
            self.logger.error(f"Error while parsing Aegis database. Error: {err}")
            raise
        except Exception as err:
            self.logger.error(f"Uknown error while trying to load Aegis database. Error: {err}")
            raise


    def new_database(self):
        self.logger.info("Creating new database")
        self.database = {"files": {}, "backups": []}

    def load(self):
        try:
            with open(self.db_file, "r+") as file:
                self.database = json.load(file)
            self.logger.debug(f"Successfully loaded DB file: {self.db_file}")
        except:
            raise # unsure where to handle DB loading errors; letting initialize error out currently
        
    def save(self):
        try:
            with open(self.db_file, "w+") as file:
                json.dump(self.database, file, indent=4, sort_keys=True)
        except Exception as err:
            self.logger.error(f"Failed to save database. There may be missing data on next start. Err: {err}")
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

    def list_files(self):
        return self.database["files"].keys()

    # gets the latest time when a snapshot was taken
    def get_latest_snapshot(self):
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
    
    def get_pit_file_hash(self, filename, timestamp):
        backups = self.database["files"][filename]["backups"]
        for b_timestamp, hash in backups.items():
            if timestamp >= int(b_timestamp):
                return hash
        return None


    def get_pit_file_timestamp(self, filename, timestamp):
        backups = self.database["files"][filename]["backups"]
        for b_timestamp, hash in backups.items():
            if timestamp >= int(b_timestamp):
                return b_timestamp
        return None