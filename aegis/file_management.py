import os, shutil, subprocess, logging
from aegis import utilities

class FileManagement:

    def __init__(self, current_time, config):
        self.logger = logging.getLogger("AegisFM")
        self.current_time = current_time
        self.staging_path = f"/tmp/aegis/{current_time}"
        self.snapshot_path = config["backup_storage_path"]
        self.changed_files = 0
        os.makedirs(self.staging_path, exist_ok=True)
        return
    
    def stage_file_for_backup(self, filename, hash):
        self.logger.debug(f"Adding file '{filename}' with hash '{hash} to snapshot.")
        path = f"{self.staging_path}/{hash[0:2]}/{hash[2:4]}/"
        os.makedirs(path, exist_ok=True)
        shutil.copy(filename, f'{path}/{hash}')
        self.changed_files += 1

    def create_snapshot(self):
        if self.changed_files > 0:
            # FIXME
            test = subprocess.Popen(f"cd {self.staging_path} && gtar cf - . | pigz > {self.snapshot_path}/{self.current_time}.tar.gz", shell=True)

    def delete_snapshot(self):
        return

    def get_snapshot_details(self):
        self.logger.info(f"{self.changed_files} files were updated or new.")

    def restore(self, restore_map):
        # FIXME
        # this is insanely ugly and mostly a PoC still; need to flesh out a more efficient and elegant way
        for snapshot in restore_map.keys():
            files_needed = []
            directories_to_make = []
            hash_to_name_matrix = []
            for file in restore_map[snapshot]:
                self.logger.info(f"Restoring file {file}.")
                hash, filename = file
                path_in_archive = f"./{hash[0:2]}/{hash[2:4]}"
                files_needed.append(f"{path_in_archive}/{hash}")
                destination_folder = "/".join(filename.split("/")[0:-1])
                if destination_folder not in directories_to_make:
                    directories_to_make.append(destination_folder)
                hash_to_name_matrix.append((f"{path_in_archive[2:]}/{hash}", filename))
            self.extract_from_snapshot(snapshot, files_needed)
            self.create_destination_restore_folders(directories_to_make)

            for file in hash_to_name_matrix:
                hash, destination = file
                temp_location = f"{self.staging_path}/{hash}"
                self.restore_file(temp_location, destination)
               

    
    def extract_from_snapshot(self, snapshot, files):
        command = f"cd {self.staging_path} && gtar -xzvf {self.snapshot_path}/{snapshot}.tar.gz {' '.join(files)}" 
        utilities.run_command(command).wait()
    
    def create_destination_restore_folders(self, folders):
        command_mkdir = f"mkdir -p {' '.join(folders)}"
        utilities.run_command(command_mkdir).wait()

    def restore_file(self, file, destination):
        command_copy = f"cp {file} {destination}"
        utilities.run_command(command_copy)
