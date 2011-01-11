from pecan                          import configuration
from pecancelery.app                import base_app
from pecancelery.bin.celeryd        import CeleryCommand

import os
import unittest

class TestCeleryWorker(unittest.TestCase):
    
    def setUp(self):
        import sys

        test_config_d = os.path.join(os.path.dirname(__file__), 'configs')

        if test_config_d not in sys.path:
            sys.path.append(test_config_d)    
    
    def test_queue_parse(self):
        """
        Ensure that if the configuration file includes an
        explicit list of queues, it's used for CELERYD_QUEUES
        """        
        conf = configuration.initconf()
        conf.update_with_module('queues')        
        
        c = CeleryCommand('celeryd')
        c.config = conf
        
        self.assertEqual(c.determine_queues(), 'example,testing123')
        
    def test_queue_autodiscover(self):
        """
        Ensure that if the configuration file *does not* include an
        explicit list of queues, a list of queues is auto-discovered.
        """        
        path = os.path.join(os.path.dirname(__file__), 'configs', 'discovery.py')
        configuration.set_config(path)  
        
        conf = base_app.conf

        c = CeleryCommand('celeryd')
        c.config = conf

        self.assertEqual(c.determine_queues(), 'default,math')