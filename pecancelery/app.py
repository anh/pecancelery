from celery                 import app
from pecancelery.loader     import LOADER_ALIAS

__all__ = ['PecanTaskFactory', 'task', 'conf', 'base_app']

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
            self.__app__ = PecanCeleryApp(loader=LOADER_ALIAS)
        return self.__app__

class BaseClassFactory(object):
    
    __task__ = None
    
    @property
    def instance(self):
        if self.__task__ is None:
            base = base_app.create_task_cls()
            from celery.task.base import TaskType
            
            class PecanTask(base):
                
                __subclasses__ = []
                
                class __metaclass__(TaskType):
                    def __init__(cls, name, bases, ns):
                        if name != 'PecanTask':
                            cls.__subclasses__.append(cls)
                        TaskType.__init__(cls, name, bases, ns)
        
            self.__task__ = PecanTask
            
        return self.__task__
        
base_app = BaseAppFactory().instance

# Exposed
PecanTaskFactory = BaseClassFactory()
task = base_app.task
conf = base_app.conf