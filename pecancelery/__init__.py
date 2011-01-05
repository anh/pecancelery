from app import PecanTaskFactory, task

VERSION = (0, 0, 1)

__version__ = ".".join(map(str, VERSION[0:3]))
__author__ = "Ryan Petrello"
__author_email__ = "ryan [at] ryanpetrello [dot] com"

PecanTask = PecanTaskFactory.instance