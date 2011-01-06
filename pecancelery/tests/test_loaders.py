from pecancelery    import loader, app
from celery         import loaders

import unittest


class TestLoader(unittest.TestCase):
    
    def setUp(self):
        self.loader = loader.PecanLoader()
    
    def test_loader_cls(self):
        self.assertEqual(loaders.get_loader_cls(loader.LOADER_ALIAS), self.loader.__class__)
        
    def test_apploader(self):
        base_app = app.BaseAppFactory().instance
        self.assertEqual(base_app.loader.__class__, self.loader.__class__)