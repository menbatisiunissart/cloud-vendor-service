#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='cloud-vendor-service',
    version='0.0.11',
    description='Cloud vendor service (AWS, Google Cloud...)',
    author='',
    author_email='',
    # REPLACE WITH YOUR OWN GITHUB PROJECT LINK
    url='https://github.com/menbatisiunissart/cloud-vendor-service',
    install_requires = ['python-dotenv==0.21.0', 'sagemaker==2.109.0'],
    packages=find_packages(),
)

