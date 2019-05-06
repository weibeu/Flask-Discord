"""
Flask-Discord
-------------

An Discord OAuth2 flask extension.
"""


from setuptools import setup


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
    install_requires=[
        'Flask',
        'requests_oauthlib',
    ],
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
