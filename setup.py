import distutils
import os

from setuptools import setup, find_packages

# Copy the contents of the `models` directory to the `src/seir` directory.
# Note: the idea is to be able to package our model files without the need for
#       our original `models` directory to be under our `src/seir` directory.

CWD = os.getcwd()

distutils.dir_util.copy_tree(CWD + '/models', CWD + '/src/seir/models')

# Deploy our package.

setup(
    author='Alan Garny',
    author_email='a.garny@auckland.ac.nz',
    description='OpenCOR-based Python package to model Covid-19 using the SEIR model',
    license='Apache 2.0',
    name='seir',
    packages=find_packages('src'),
    package_data={
        'seir': ['models/*'],
    },
    package_dir={'': 'src'},
    url='https://github.com/ABI-Covid-19/seir',
    version='0.2.0',
)
