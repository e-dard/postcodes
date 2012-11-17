"""
Postcodes
---------

A simple library for getting access to UK Postcode data.
"""
from setuptools import setup

setup(
    name='Postcodes',
    version='0.1',
    url='http://github.com/e-dard/postcodes',
    license='WTFPL',
    author='Edward Robinson',
    author_email='me@eddrobinson.net',
    description='A simple library for getting access to UK Postcode data,' \
                'including latitide and longitude and administrative ' \
                'information. You can also search for other postcodes within' \
                'a distance of a point or other postcode.',
    long_description=__doc__,
    py_modules=['postcodes'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[],
    tests_require=['mock'],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: Other/Proprietary License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
