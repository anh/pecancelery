from pecan                      import configuration
from configs.sampleproj.tasks   import AddTask, subtract

import os
import unittest


class TestRun(unittest.TestCase):
    
    def test_run(self):
        path = os.path.join(os.path.dirname(__file__), 'configs', 'discovery.py')
        configuration.set_config(path)        
        
        result = AddTask.delay(1, 2)
        self.assertEqual(result.result, 3)
        
        result = subtract(6, 2)
        self.assertEqual(result, 4)