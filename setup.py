from setuptools import setup, find_packages

setup(
    name='g-rpc',
    version='1.2.0',
    description="A simple client and server for rpc methods",
    packages=find_packages(),
    install_requires=[
        'pika>=1.3.2',
    ],
)
