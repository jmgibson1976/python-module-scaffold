import sys
import os
import shutil
import fileinput
import subprocess
from configparser import ConfigParser

if sys.version_info[0] < 3 and sys.version_info[1] < 8:
    raise Exception("Python3.8 or higher required.")

# get current path
os.chdir(os.path.dirname(os.path.abspath(__file__)))
current = os.getcwd()

# template folder directories containing templates
# that will be copied into new module
root_files_path = os.path.join(current, 'module-root-files')
config_files_path = os.path.join(current, 'module-config-files')
src_files_path = os.path.join(current, 'module-src-files')

# get expected project path
project_path = input(f'Enter project directory or hit enter for default [{current}]: ')

if not project_path:
    project_path = current

# if path doesnt exist, create it
if not os.path.exists(project_path):
    os.makedirs(project_path, exist_ok=True)

# get project name
project_name = input('Enter project name: ')

project_path = os.path.join(project_path, project_name.lower())
src_path = os.path.join(project_path, project_name.lower())
configs_path = os.path.join(project_path, 'configs')
logs_path = os.path.join(project_path, 'logs')

# confirm install
confirmation = input(f'Installing to {project_path}, [Y/n]?: ')

if confirmation.lower() != 'y':
    print('Exiting...')
    exit()

# begin scaffolding directories
try:
    os.mkdir(project_path)
    os.mkdir(src_path)
    os.mkdir(configs_path)
    os.mkdir(logs_path)

    # copy root files
    src = os.listdir(root_files_path)
    dst = project_path + os.sep

    for files in src:
        src_file = os.path.join(root_files_path, files)
        shutil.copy(src_file, dst)

    # copy config files
    src = os.listdir(config_files_path)
    dst = configs_path + os.sep

    for files in src:
        src_file = os.path.join(config_files_path, files)
        shutil.copy(src_file, dst)

    # copy config template to config.ini
    shutil.copy(os.path.join(dst,'config.ini.template'), os.path.join(dst, 'config.ini'))

    # copy src files
    src = os.listdir(src_files_path)
    dst = src_path + os.sep

    for files in src:
        src_file = os.path.join(src_files_path, files)
        shutil.copy(src_file, dst)

    # create README in logs directory so it makes it into git repo
    os.chdir(logs_path)
    fp = open('README.md', 'w')
    fp.close()

    # ch dir to project root dir
    os.chdir(project_path)

    # update setup.py
    # https://stackoverflow.com/questions/17140886/how-to-search-and-replace-text-in-a-file
    with fileinput.FileInput('setup.py', inplace=True) as file:
        for line in file:
            print(line.replace('{project_name}', project_name.lower()).rstrip('\n'))


    # update & save config.ini
    os.chdir(configs_path)
    config = ConfigParser()
    config.read('config.ini')
    config.set('Default', 'application', project_name)

    with open('config.ini', 'w') as configfile:
        config.write(configfile)

    # ch dir to project root dir
    os.chdir(project_path)

    # Initialize Git?
    confirmation_git = input(f'Would you like to initialize Git on this project, [Y/n]?: ')

    if confirmation_git.lower() == 'y':
        response = subprocess.run(["git", "init"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # capture data from stdout
        print(response.stdout.decode('utf-8'))

    print ('Scaffold complete!\n')
    
except Exception as e:
    print(e)
