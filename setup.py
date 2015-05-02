from setuptools import setup, find_packages

setup(
    name = 'port_dashboard',
    version = '1.0',
    packages = find_packages(),

    package_data = {
        '': ['LICENSE', 'README.md'],
    },

    # PyPI metadata
    description = 'generate a port to-do list from C preprocessor macros',
    author = 'Michael Labbe',
    author_email = 'mike@frogtoss.com',
    url = 'https://github.com/mlabbe/port_dashboard',
#    keywords = ['logging', 'debug', 'release'],
)
