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


requirements = [
    "aiohttp==3.7.4.post0",
    "async-timeout==3.0.1",
    "attrs==21.4.0",
    "cachetools==5.0.0",
    "certifi==2021.10.8",
    "chardet==4.0.0",
    "charset-normalizer==2.0.11",
    "click==8.0.3",
    "discord.py==1.7.3",
    "Flask==2.0.2",
    "idna==3.3",
    "itsdangerous==2.0.1",
    "Jinja2==3.0.3",
    "MarkupSafe==2.0.1",
    "multidict==6.0.2",
    "oauthlib==3.2.0",
    "PyJWT==2.3.0",
    "requests==2.27.1",
    "requests-oauthlib==1.3.1",
    "typing_extensions==4.0.1",
    "urllib3==1.26.8",
    "Werkzeug==2.0.3",
    "yarl==1.7.2",
]


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
    version=__get_version(),
    url='https://github.com/thec0sm0s/Flask-Discord',
    license='MIT',
    author='□ | The Cosmos',
    author_email='deepakrajko14@gmail.com',
    description='Discord OAuth2 extension for Flask.',
    long_description=__doc__,
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=requirements,
    extras_require=extra_requirements,
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
