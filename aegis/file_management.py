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