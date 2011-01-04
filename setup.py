import distribute_setup
distribute_setup.use_setuptools()
from setuptools import setup

tests_require = ['pytest']

setup(
    name = "pecan-celery",
    version = "0.0.1",
    packages = ['pecan-celery'],
    include_package_data=True,
    scripts=['bin/celery'],
    # metadata 
    author = "Ryan Petrello",
    author_email = "ryan [at] ryanpetrello [dot] com",
    description = "Celery integration for pecan",
    long_description = open('README.rst').read(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Topic :: System :: Distributed Computing',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7'
    ],
    license = "MIT",
    keywords = "pecan, celery, framework, task queue, asynchronous, rabbitmq, amqp, queue, distributed",
    url = "https://github.com/ryanpetrello/pecan-celery",

)