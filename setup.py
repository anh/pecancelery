try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

#
# determine requirements
#
requirements = [
  "pecan",
  "celery >= 2.2"
]

setup(
    name                    = "pecancelery",
    version                 = "0.0.1a1",
    include_package_data    = True,
                            
    # metadata              
    author                  = "Ryan Petrello",
    author_email            = "ryan [at] ryanpetrello [dot] com",
    description             = "Celery integration for pecan",
    long_description        = open('README.rst').read(),
    packages                = find_packages(exclude=['ez_setup', 'tests']),
    classifiers             = [
        'Development Status :: 3 - Alpha',
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
                            
    install_requires        = requirements,
    entry_points            = """
    [paste.paster_command]
    pecan-celeryd       = pecancelery.commands.celeryd:CeleryCommand
    pecan-celerystop    = pecancelery.commands.celerystop:CeleryCommand
    """
)