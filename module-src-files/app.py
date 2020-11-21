import config
import logging
import os
import time

def _logging():
    """Setup logging configuration for the application here"""

    timestr  = time.strftime("%Y%m%d")
    filename = os.path.join(config.LOGS_DIR, timestr + '.log')

    logging.basicConfig(filename=filename, format='%(asctime)s %(levelname)s: %(message)s', level=logging.INFO)

def run(args):

    # initialize logging setup
    _logging()

    print('Running...')