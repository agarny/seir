from setuptools import setup, find_packages

setup(
    author='Alan Garny',
    author_email='a.garny@auckland.ac.nz',
    description='OpenCOR-based Python script to model Covid-19 using the SEIR model',
    license='Apache 2.0',
    name='seir',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/ABI-Covid-19/seir',
    version='0.2.0',
)
