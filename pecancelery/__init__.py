import os

VERSION = (0, 0, 1)

__version__ = ".".join(map(str, VERSION[0:3]))
__author__ = "Ryan Petrello"
__author_email__ = "ryan [at] ryanpetrello [dot] com"

def init_loader():
    os.environ.setdefault("CELERY_LOADER", "pecancelery.loader.PecanLoader")

# Importing this module enables the PecanLoader
init_loader()