from setuptools import setup, find_packages

setup(
    name='g-rpc',
    version='1.1.2',
    packages=find_packages(),
    install_requires=[
        'pika>=1.3.2',
    ],
)
