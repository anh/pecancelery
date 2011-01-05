from celery.loaders.base        import BaseLoader
import warnings

import imp

__all__ = ['PecanLoader']
    
def autodiscover(module):
    name = 'tasks'
    try:
        app_path = module.__path__
    except AttributeError:
        return

    try:
        imp.find_module(name, app_path)
    except ImportError:
        return

    return "%s.%s" % (module.__name__, name)


class ConfigStruct(object):
    def __init__(self, **kwargs): 
        self.__dict__.update(kwargs)
        

class PecanLoader(BaseLoader):
    _db_reuse = 0
    
    def _parse_config(self):
        from pecan import conf
        c = getattr(conf, 'celery', {})
        
        # If CELERY_IMPORTS isn't specified, try to autodiscover celery tasks
        if c.get('CELERY_IMPORTS') is None:
            c['CELERY_IMPORTS'] = tuple([filter(None, autodiscover(module)) for module in conf.app.modules])
            
        c['CELERY_ROUTES'] = ('pecancelery.loader.PecanTaskRouter',)
        
        if not len(c['CELERY_IMPORTS']):
            warnings.warn("Could not auto-discover tasks in your Pecan project.  Please manually specify CELERY_IMPORTS in your Pecan configuration file.")
        
        return ConfigStruct(**c)

    def read_configuration(self):
        self.configured = True
        return self._parse_config()
        
    def on_worker_init(self):
        """Called when the worker starts."""
        self.import_default_modules()
        
    @property
    def conf(self):
        return self.read_configuration()
        
class PecanTaskRouter(object):

    def route_for_task(self, task, args=None, kwargs=None):
        try:
            parts = task.rsplit('.', 1)
            m = __import__(parts[0])
            for n in task.split(".")[1:]:
                m = getattr(m, n)
            return getattr(m, 'queue', None)
        except:
            pass
        return None
