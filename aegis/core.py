import os, shutil, aegis.database as database, aegis.file_management as file_management, logging
import multiprocessing
from multiprocessing import Pool, freeze_support
from time import time
from aegis import utilities



class Core:
    BACKUP = "backup"
    RESTORE = "restore"

    def __init__(self, current_time, config, command):
        self.logger = logging.getLogger("AegisCore")
        self.logger.debug(f"Received command: {command}")
        self.fm = file_management.FileManagement(current_time, config)
        self.db = database.Database(config)
        if command == Core.BACKUP:
            self.logger.info("Starting backup.")
            self.db.record_backup(current_time)
            self.backup(config["folders_to_backup"][0])
            self.fm.create_snapshot()
            self.fm.get_snapshot_details()
            self.db.commit_backup()
            self.db.save()
        elif command == Core.RESTORE:
            self.logger.info("Starting restore.")
            self.restore_most_recent()

    def restore_file(self, filename, timestamp):
        return


    def restore_most_recent(self):
        restore_map = {}
        for file in self.db.list_files():
            archive = self.db.get_latest_file_timestamp(file)
            if archive not in restore_map:
                self.logger.debug(f"Adding archive {archive} to RestoreMap")
                restore_map[archive] = []
                restore_map[archive].append((self.db.get_latest_file_hash(file), file))
            else:
                restore_map[archive].append((self.db.get_latest_file_hash(file), file))
        self.fm.restore(restore_map)


    def backup(self, world_directory):
        self.logger.debug(f"Scanning '{world_directory}' for changes...")
        file_list = []
        for (dirpath, dirs, files) in os.walk(world_directory):
            self.logger.debug(f"Walking path '{dirpath}' for files.")
            for name in files:
                file_list.append(os.path.join(dirpath, name))

        results = []
        with Pool(5) as p:
            results = p.map(utilities.md5, file_list)


        for index, filename in enumerate(file_list):
            if not self.db.file_exists(filename):
                # first time seeing file, let's create an entry
                self.logger.debug(f"{filename} is new!")
                self.db.create_file(filename, results[index])
                self.fm.stage_file_for_backup(filename, results[index])
            else:
                # only copy the file if it's new
                if self.db.get_latest_file_hash(filename) == results[index]:
                    self.logger.debug(f"{filename} is the same.")
                else:
                    self.fm.stage_file_for_backup(filename, results[index])
                    self.db.update_file(filename, results[index])
                    self.logger.debug(f"{filename} has changed!")

if __name__ == '__main__':
    freeze_support()