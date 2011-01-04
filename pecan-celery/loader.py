from celery.loaders.base    import BaseLoader

__all__ = []

def _parse_config():
    """Load configuration from pecan config."""
    
    from pecan import conf
    c = getattr(conf, 'celery', {})
    c['CELERY_ROUTES'] = ('pecancelery.loader.PecanTaskRouter',)

    return ConfigStruct(**c)

class ConfigStruct(object):
    def __init__(self, **kwargs): 
        self.__dict__.update(kwargs)

class PecanLoader(BaseLoader):
    _db_reuse = 0

    def read_configuration(self):
        self.configured = True
        return _parse_config()
        
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
            return m.queue or None
        except:
            pass
        return None
