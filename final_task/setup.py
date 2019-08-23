from setuptools import setup, find_packages

setup(
    name='pycalc',
    description='pure line-command calculator',
    version='ver:0.9',
    author='pilat egor',
    author_email='pilat.egor@gmail.com',
    packages=find_packages(),
    entry_points={
        'console_scripts': ['pycalc = pycalc:calc']
    }
)
