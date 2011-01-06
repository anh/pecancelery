from celery.loaders.base        import BaseLoader

import imp

__all__ = ['PecanLoader', 'LOADER_ALIAS']

LOADER_ALIAS = 'pecancelery.loader.PecanLoader'
    
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
        
        c = getattr(conf, 'celery', None)
        if c is None:
            return {}
        c = dict(c)
        
        # If CELERY_IMPORTS isn't specified, try to autodiscover celery tasks
        if c.get('CELERY_IMPORTS') is None:
            modules = getattr(conf.app, 'modules', [])
            imports = [filter(None, autodiscover(module)) for module in modules]
            if len(imports):
                c['CELERY_IMPORTS'] = tuple(imports)
            
        c['CELERY_ROUTES'] = ('pecancelery.loader.PecanTaskRouter',)
        
        return c

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
