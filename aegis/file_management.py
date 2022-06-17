import os, shutil, subprocess, logging

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

    def restore_snapshot(self, restore_map):
        # FIXME
        # this is insanely ugly and mostly a PoC still; need to flesh out a more efficient and elegant way
        for archive in restore_map.keys():
            files_needed = []
            directories_to_make = []
            hash_to_name_matrix = []
            for file in restore_map[archive]:
                self.logger.debug(f"Restoring file {file}.")
                hash = file[0]
                filename = file[1]
                path_in_archive = f"./{hash[0:2]}/{hash[2:4]}"
                files_needed.append(f"{path_in_archive}/{hash}")
                directories_to_make.append("/".join(filename.split("/")[0:-1]))
                hash_to_name_matrix.append((f"{path_in_archive[2:]}/{hash}", filename))
            command = f"cd {self.staging_path} && gtar -xzvf {self.snapshot_path}/{archive}.tar.gz {' '.join(files_needed)}" 
            self.logger.debug(f"Running command: {command}")
            test = subprocess.Popen(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
            test.wait()
            command_mkdir = f"mkdir -p {' '.join(directories_to_make)}"
            self.logger.debug(f"Running command: {command_mkdir}")
            test = subprocess.Popen(command_mkdir, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
            test.wait()
            for file in hash_to_name_matrix:
                command_copy = f"cp {self.staging_path}/{file[0]} {file[1]}"
                self.logger.debug(f"Running command: {command_copy}")
                test = subprocess.Popen(command_copy, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)