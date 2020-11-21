import configparser
import os

# Project Directories
ROOT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
LOGS_DIR = os.path.join(ROOT_DIR, 'logs')
CONFIGS_DIR = os.path.join(ROOT_DIR, 'configs')

# File Paths
APP_CONFIG_PATH = os.path.join(CONFIGS_DIR, 'config.ini')

config = configparser.ConfigParser()
config.read(APP_CONFIG_PATH)