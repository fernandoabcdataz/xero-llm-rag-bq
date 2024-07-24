from setuptools import setup, find_packages

setup(
    name='xero_pipeline',
    version='0.1',
    install_requires=[
        'apache-beam[gcp]',
        'oauthlib',
        'requests',
        'json',
        'logging',
        'requests-oauthlib',
        'google-cloud-storage',
        'google-auth',
        'google-auth-oauthlib',
    ],
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'xero-pipeline=xero_api.xero:run_pipeline',
        ],
    },
)