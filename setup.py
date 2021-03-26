from setuptools import setup

setup(
    name='applython',
    version='0.1.0',
    description='efficiently and dynamically render cover letters.',
    author='Joshua Ruf',
    url='https://github.com/joshua-ruf/applython',
    py_modules=['app'],
    install_requires=[
        'Click',
        'Flask',
        'Flask-Flatpages',
        'Frozen-Flask',
        'pdfkit'
    ],
    entry_points={
        'console_scripts': [
            'applython = app:cli',
        ],
    },
)
