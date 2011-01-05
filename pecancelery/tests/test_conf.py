import os
import celery
import unittest
from pecan import configuration

class TestConf(unittest.TestCase):
    
    def setUp(self):
        import sys

        test_config_d = os.path.join(os.path.dirname(__file__), 'configs')

        if test_config_d not in sys.path:
            sys.path.append(test_config_d)
            
    def test_defaults(self):
        """
        Ensure that if the configuration file includes no celery
        config, the parsed config object is identical to
        celery's default config object
        """
        conf = configuration.initconf()
        conf.update_with_module('empty')

        from pecancelery import PecanTask, conf
        app = celery.Celery()
        for k, v in app.loader.conf.items():
            self.assertEqual(dict(conf)[k], v)
            
    def test_single_config(self):
        """
        Ensure that if the configuration file includes no celery
        config, the parsed config object is identical to
        celery's default config object
        """
        conf = configuration.initconf()
        conf.update_with_module('empty')

        from pecancelery import PecanTask, conf
        app = celery.Celery()
        for k, v in app.loader.conf.items():
            if k == 'BROKER_HOST':
                self.assertEqual(v, 'example.com')
            else:
                self.assertEqual(dict(conf)[k], v)        
        