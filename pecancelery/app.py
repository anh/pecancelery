from celery import app

__all__ = ['PecanTaskFactory', 'task', 'conf']

class PecanCeleryApp(app.App):
    
    def task(self, *args, **options):
        options['base'] = PecanTaskFactory.instance
        return super(PecanCeleryApp, self).task(*args, **options)
    
    @property
    def conf(self):
        """Current configuration (dict and attribute access)."""
        return self._get_config()

class BaseAppFactory(object):
    
    __app__ = None
    
    @property
    def instance(self):
        if self.__app__ is None:
            self.__app__ = PecanCeleryApp(loader='pecancelery.loader.PecanLoader')
        return self.__app__

class BaseClassFactory(object):
    
    __task__ = None
    
    @property
    def instance(self):
        if self.__task__ is None:
            self.__task__ = base_app.create_task_cls()
        return self.__task__
        
base_app = BaseAppFactory().instance

# Exposed
PecanTaskFactory = BaseClassFactory()
task = base_app.task
conf = base_app.conf