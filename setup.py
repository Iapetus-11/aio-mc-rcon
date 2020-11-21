from aiomcrcon import __version__
import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='aio-mc-rcon',
    version=__version__,
    author='Iapetus-11',
    description='An async library/wrapper for interacting with remote consoles on Minecraft Java Edition servers',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Iapetus-11/aio-mc-rcon',
    packages=setuptools.find_packages(),
    data_files=[
        ('', ['LICENSE'])
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6'
)
