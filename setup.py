from setuptools import setup, find_packages

setup(name='subc_sender',
    version='1.0',
    packages=find_packages(),
    install_requires=[],
    extras_require={  # Optional
        'test': ['pytest'],
    },
)
