from setuptools import setup, find_packages

setup(
    name='xero_pipeline',
    version='0.1',
    install_requires=[
        'apache-beam[gcp]',
        'oauthlib',
        'requests-oauthlib',
        'google-cloud-storage',
    ],
    packages=find_packages(),
)