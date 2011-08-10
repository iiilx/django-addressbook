# -*- coding: utf-8 -*-
from distutils.core import setup
from setuptools import find_packages

setup(
    name='django-addressbook',
    version='0.1.1',
    author=u'Ben Lee',
    author_email='ben86lee@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    install_requires = [
    'vobject',
    'django-uni-form',
    ],
    url='https://github.com/iiilx/addressbook',
    license='BSD license, see LICENSE.txt',
    description='A django app that allows users to create contact groups and contacts, as well as views for displaying a contact in hcard format, downloading a vcard for the contact, a gravatar, and a QR code.', 
    long_description=open('README.txt').read(),
    zip_safe=False,
)
