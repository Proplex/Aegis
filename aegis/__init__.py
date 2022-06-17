import logging, time, os
from aegis.core import Core
from aegis.configuration import Configuration
from aegis import core, configuration

def initialize():
    current_time = int(time.time())
    log_level = os.environ.get('LOGLEVEL', 'INFO').upper()
    logging.basicConfig(format='%(asctime)s [%(levelname)s] [%(name)s] %(message)s',level=log_level)
    config = Configuration("config.yml").get()
    aegis = Core(current_time, config, Core.RESTORE)