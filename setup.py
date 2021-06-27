"""
Flask-Discord
-------------

An Discord OAuth2 flask extension.
"""

import re
import os

from setuptools import setup, find_packages


def __get_version():
    with open("flask_discord/__init__.py") as package_init_file:
        return re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', package_init_file.read(), re.MULTILINE).group(1)


def __get_requirements():
    with open("requirements.txt") as file:
        return file.readlines()


version = __get_version()
requirements = __get_requirements()


on_rtd = os.getenv('READTHEDOCS') == 'True'
if on_rtd:
    requirements.append('sphinxcontrib-napoleon')
    requirements.append('Pallets-Sphinx-Themes')

extra_requirements = {
    'docs': [
        'sphinx==1.8.3'
    ]
}


setup(
    name='Flask-Discord',
    version=version,
    url='https://github.com/weibeu/Flask-Discord',
    license='MIT',
    author='Weibeu',
    author_email='deepakrajko14@gmail.com',
    description='Discord OAuth2 extension for Flask.',
    long_description=__doc__,
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=requirements,
    extra_requirements=extra_requirements,
    classifiers=[
        'Framework :: Flask',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
