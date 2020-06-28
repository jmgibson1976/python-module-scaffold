import configparser
import os

# Project Root
ROOT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')

# File Paths
CONFIG_PATH = os.path.join(ROOT_DIR, 'config.ini')

config = configparser.ConfigParser()
config.read(CONFIG_PATH)