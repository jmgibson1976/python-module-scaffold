import sys
import os
import shutil
import fileinput
import subprocess
from configparser import ConfigParser

if sys.version_info[0] < 3 and sys.version_info[1] < 5:
    raise Exception("Python3.5 or higher required.")

# get current path
os.chdir(os.path.dirname(os.path.abspath(__file__)))
current = os.getcwd()

root_files_path = current + '/' + 'module-root-files'
src_files_path = current + '/' + 'module-src-files'

# get expected project path
project_path = input(f'Enter project directory or hit enter for default [{current}]: ')

if not project_path:
    project_path = current

# get project name
project_name = input('Enter project name: ')

project_path = os.path.join(current, project_name)
src_path = os.path.join(project_path, project_name.lower())
docs_path = os.path.join(project_path, 'docs')
tests_path = os.path.join(project_path, 'tests')

# confirm install
confirmation = input(f'Installing to {project_path}, [Y/n]?: ')

if confirmation.lower() != 'y':
    print('Exiting...')
    exit()

# begin scaffolding directories
try:
    os.mkdir(project_path)
    os.mkdir(src_path)
    os.mkdir(docs_path)
    os.mkdir(tests_path)

    # copy root files
    src = os.listdir(root_files_path)
    dst = project_path + os.sep

    for files in src:
        src_file = root_files_path + os.sep + files
        shutil.copy(src_file, dst)

    # copy src files
    src = os.listdir(src_files_path)
    dst = src_path + os.sep

    for files in src:
        src_file = src_files_path + os.sep + files
        shutil.copy(src_file, dst)

    # ch dir to project root dir
    os.chdir(project_path)

    # update setup.py
    # https://stackoverflow.com/questions/17140886/how-to-search-and-replace-text-in-a-file
    with fileinput.FileInput('setup.py', inplace=True) as file:
        for line in file:
            print(line.replace('{project_name}', project_name).rstrip('\n'))

    # update & save config.ini
    config = ConfigParser()
    config.read('config.ini')
    config.set('Default', 'application', project_name)

    with open('config.ini', 'w') as configfile:
        config.write(configfile)

    # Initialize Git?
    confirmation_git = input(f'Would you like to initialize Git on this project, [Y/n]?: ')

    if confirmation_git.lower() == 'y':
        response = subprocess.run(["git", "init"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # capture data from stdout
        print(response.stdout.decode('utf-8'))

    print ('Scaffold complete!\n')
    
except Exception as e:
    print(e)
