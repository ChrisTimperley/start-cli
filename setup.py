import glob
import setuptools

setuptools.setup(
    name='start_cli',
    version='0.0.1',
    description='Provides a command-line interface to START',
    author='Chris Timperley',
    author_email='christimperley@gmail.com',
    url='https://github.com/ChrisTimperley/start-cli',
    install_requires=[
        'start-image',
        'start-core',
        'start-repair',
        'tabulate',
        'cement'
    ],
    python_requires='>=3.5',
    packages=['start_cli'],
    entry_points = {
        'console_scripts': [ 'start-cli = start_cli:main' ]
    }
)
