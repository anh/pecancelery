from setuptools import setup

import pecancelery as distmeta

#
# determine requirements
#
requirements = [
  "pecan",
  "celery >= 2.2"
]

setup(
    name                    = "pecancelery",
    version                 = distmeta.__version__,
    packages                = ['pecancelery'],
    include_package_data    = True,
                            
    # metadata              
    author                  = distmeta.__author__,
    author_email            = distmeta.__author_email__,
    description             = "Celery integration for pecan",
    long_description        = open('README.rst').read(),
    classifiers             = [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Topic :: System :: Distributed Computing',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7'
    ],
    license                 = "BSD",
    keywords                = "pecan, celery, framework, task queue, asynchronous, rabbitmq, amqp, queue, distributed",
    url                     = "https://github.com/ryanpetrello/pecancelery",
                            
    scripts                 = ['bin/celery'],
    install_requires        = requirements
)