import os, shutil, subprocess

class FileManagement:

    def __init__(self, current_time):
        self.current_time = current_time
        self.staging_path = f"/tmp/aegis/{current_time}"
        self.snapshot_path = "/Users/david/work/aigis/aegis/"
        self.changed_files = 0
        os.makedirs(self.staging_path, exist_ok=True)
        return
    
    def stage_file_for_backup(self, filename, hash):
        path = f"{self.staging_path}/{hash[0:2]}/{hash[2:4]}/"
        os.makedirs(path, exist_ok=True)
        shutil.copy(filename, f'{path}/{hash}')
        self.changed_files += 1

    def create_snapshot(self):
        if self.changed_files > 0:
            test = subprocess.Popen(f"cd {self.staging_path} && gtar cf - . | pigz > {self.snapshot_path}/{self.current_time}.tar.gz", shell=True)
    def delete_snapshot(self):
        return