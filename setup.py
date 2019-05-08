"""
Flask-Discord
-------------

An Discord OAuth2 flask extension.
"""

import re
import os

from setuptools import setup


def __get_version():
    with open("image_processor_client/__init__.py") as package_init_file:
        return re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', package_init_file.read(), re.MULTILINE).group(1)


requirements = [
        'Flask',
        'requests_oauthlib',
    ]


on_rtd = os.getenv('READTHEDOCS') == 'True'
if on_rtd:
    requirements.append('sphinxcontrib-napoleon')

extra_requirements = {
    'docs': [
        'sphinx==1.8.3'
    ]
}


setup(
    name='Flask-Discord',
    version='0.0.1',
    url='',
    license='BSD',
    author='□ | The Cosmos',
    author_email='deepakrajko14@gmail.com',
    description='',
    long_description=__doc__,
    packages=['flask_discord'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=requirements,
    extra_requirements=extra_requirements,
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
