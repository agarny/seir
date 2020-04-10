from setuptools import setup

setup(
    author='Alan Garny',
    author_email='a.garny@auckland.ac.nz',
    description='OpenCOR-based Python script to model Covid-19 using the SEIR model',
    scripts=[
        'src/seir.py'
    ],
    license='Apache 2.0',
    name='seir',
    url='https://github.com/ABI-Covid-19/seir',
    version='0.1.0',
)
