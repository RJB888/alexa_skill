"""The setup for AIM project in python."""

from setuptools import setup

setup(
    name="AIM: Alexa Intelligent Messenger",
    description="A smart messaging skill for Alexa.",
    version=1.0,
    author="John Jensen, Marco Zangari, Robert Bronson, Darren Haynes",
    author_email="",
    license='MIT',
    py_modules=[],
    install_requires=['boto3'],
    extras_require={'test':
                    [
                        '--target=/home/darren/CodeFellows/alexa_skill/lib rx',
                        'pytest',
                        'pytest-cov',
                        'tox']
                    },
    entry_points={
        'console_scripts': []
    }
)
