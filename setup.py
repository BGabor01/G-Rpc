from setuptools import setup, find_packages

setup(
    name='g_rpc',
    version='1.0',
    packages=find_packages(),
    install_requires=[
        'pika>=1.3.2',
    ],
)