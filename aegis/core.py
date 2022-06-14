#!/bin/python3
import hashlib, os, shutil, aegis.database as database, aegis.file_management as file_management, logging
import multiprocessing
from multiprocessing import Pool, freeze_support
from time import time


def start(current_time, db, fm, config):
    db.record_backup(current_time)
    aegis(config["folders_to_backup"][0], db, fm)
    fm.create_snapshot()
    fm.get_snapshot_details()
    db.commit_backup()
    db.save()


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
    logger = logging.getLogger("AegisCore")
    logger.debug(f"Scanning '{world_directory}' for changes...")
    file_list = []
    for (dirpath, dirs, files) in os.walk(world_directory):
        logger.debug(f"Walking path '{dirpath}' for files.")
        for name in files:
            file_list.append(os.path.join(dirpath, name))

    results = []
    with Pool(5) as p:
        results = p.map(md5, file_list)


    for index, filename in enumerate(file_list):
        if not db.file_exists(filename):
            # first time seeing file, let's create an entry
            logger.debug(f"{filename} is new!")
            db.create_file(filename, results[index])
            fm.stage_file_for_backup(filename, results[index])
        else:
            # only copy the file if it's new
            if db.get_latest_file_hash(filename) == results[index]:
                logger.debug(f"{filename} is the same.")
            else:
                fm.stage_file_for_backup(filename, results[index])
                db.update_file(filename, results[index])
                logger.debug(f"{filename} has changed!")

if __name__ == '__main__':
    freeze_support()