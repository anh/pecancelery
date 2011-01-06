from pecan              import configuration
from pecancelery.app    import base_app

import os
import unittest


class TestDiscovery(unittest.TestCase):
    
    def test_autodiscovery(self):
        path = os.path.join(os.path.dirname(__file__), 'configs', 'discovery.py')
        configuration.set_config(path)        
        
        conf = base_app.conf
        self.assertEqual(conf.get('CELERY_IMPORTS'),  ('sampleproj.tasks',))