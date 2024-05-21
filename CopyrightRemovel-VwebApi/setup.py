from setuptools import setup, find_packages

setup(
    name='studio_unofficial_api',
    version='0.0.1',
    packages=find_packages(),
    install_requires=[
        "playwright==1.40.0",
        "requests==2.32.0"
    ],
)
