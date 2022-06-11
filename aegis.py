#!/bin/python3
import hashlib, os, shutil, database, file_management
from multiprocessing import Pool
from time import time


def md5(file_name):
    hash_md5 = hashlib.md5()
    with open(file_name, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def stage_file_for_backup(file_name, hash):
    hash_part1 = hash[0:2]
    hash_part2 = hash[2:4]
    path = f'/tmp/aegis/{hash_part1}/{hash_part2}/'
    os.makedirs(path, exist_ok=True)
    shutil.copy(file_name, f'{path}/{hash}')
    return True

def aegis(world_directory, db, fm):
    file_list = []



    for (dirpath, dirs, files) in os.walk(world_directory):
        for name in files:
            file_list.append(os.path.join(dirpath, name))

    results = []
    with Pool(5) as p:
        results = p.map(md5, file_list)


    for index, filename in enumerate(file_list):
        if not db.file_exists(filename):
            # first time seeing file, let's create an entry
            print(f"[AegisSnapshot] {filename} is new!")
            db.create_file(filename, results[index])
            fm.stage_file_for_backup(filename, results[index])
        else:
            # only copy the file if it's new
            if db.get_latest_file_hash(filename) == results[index]:
                print(f"[AegisSnapshot] {filename} is the same.")
            else:
                fm.stage_file_for_backup(filename, results[index])
                db.update_file(filename, results[index])
                print(f"[AegisSnapshot] {filename} has changed!")

        


if __name__ == "__main__":
    current_time = int(time())
    db = database.AegisDB("aegis_db.json")
    fm = file_management.FileManagement(current_time)
    db.record_backup(current_time)
    aegis("minecraft/world", db, fm)
    fm.create_snapshot()
    db.commit_backup()
    db.save()