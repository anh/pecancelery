import os
import celery
import unittest
from pecan              import configuration

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

        from pecancelery import conf
        app = celery.Celery()
        for k, v in app.loader.conf.items():
            self.assertEqual(dict(conf)[k], v)
            
    def test_single_config(self):
        """
        Ensure that if the configuration file includes celery-specific
        config, the parsed config object includes it
        """
        conf = configuration.initconf()
        conf.update_with_module('empty')

        from pecancelery import conf
        app = celery.Celery()
        for k, v in app.loader.conf.items():
            if k == 'BROKER_HOST':
                self.assertEqual(dict(conf)[k], 'example.com')
            else:
                self.assertEqual(dict(conf)[k], v)        
        
    def test_celery_imports_module(self):
        """
        Ensure that if CELERY_IMPORTS is specified manually in pecan config,
        it's actually used
        """     
        conf = configuration.initconf()
        conf.update_with_module('standard')

        from pecancelery import conf
        app = celery.Celery()
        for k, v in app.loader.conf.items():
            if k == 'CELERY_IMPORTS':
                self.assertEqual(dict(conf)[k], ('package.module.tasks',))

    def test_backend(self):
        """
        Ensure that if CELERY_RESULT_BACKEND is specified manually in pecan
        config, that the broker is properly set at the `app` and `task` level.
        """     
        from celery.backends.database   import DatabaseBackend
        from configs.sampleproj.tasks   import AddTask
        path = os.path.join(os.path.dirname(__file__), 'configs', 'database_backend.py')
        configuration.set_config(path)        

        task = AddTask()
        assert task.app.backend.__class__ == DatabaseBackend
        assert task.backend.__class__ == DatabaseBackend
