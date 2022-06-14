import logging, time, os
import multiprocessing
from aegis import database, file_management, core, configuration

def initialize():
    current_time = int(time.time())
    log_level = os.environ.get('LOGLEVEL', 'INFO').upper()
    logging.basicConfig(format='%(asctime)s [%(levelname)s] [%(name)s] %(message)s',level=log_level)
    config = configuration.Configuration("config.yml").get()
    fm = file_management.FileManagement(current_time, config)
    db = database.Database(config)
    core.start(current_time, db, fm, config)