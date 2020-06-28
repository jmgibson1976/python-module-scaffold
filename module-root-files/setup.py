import os
from setuptools import setup, find_packages
from {project_name}.config import config

conf = config['Default']
README = open(os.path.join(os.path.dirname(__file__), "README.md")).read()

setup(
    name=conf['application'],
    url=conf['url'],
    version=conf['version'],
    author=conf['author'],
    author_email=conf['email'],
    description='',
    keywords='',
    long_description=README,
    install_requires=[],
    packages=find_packages(),
    package_data={'': ['LICENSE']},
    include_package_data=True,
    zip_safe=False,
    classifiers=[],
    python_requires='>=3.5'
)