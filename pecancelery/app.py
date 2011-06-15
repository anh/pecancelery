from celery                 import app
from pecancelery.loader     import LOADER_ALIAS

__all__ = ['PecanTaskFactory', 'task', 'conf', 'base_app']

class PecanCeleryApp(app.App):
    
    def task(self, *args, **options):
        # Retrieve the base intance
        base = PecanTaskFactory.instance
        options['base'] = base
        
        # Pass on to the native task decorator
        f = super(PecanCeleryApp, self).task(*args, **options)
        
        #
        # Add the decorated function into our list of "autodiscovered"
        # subtasks
        #
        base.__subtasks__.append(f)
        
        #
        # If the `queue` keyword argument is specified,
        # attach it to the wrapped function
        #
        if options.get('queue'):
            setattr(f, 'queue', options['queue'])
        
        return f
    
    @property
    def conf(self):
        """Current configuration (dict and attribute access)."""
        return self._get_config()

    @property
    def backend(self):
        """Storing/retreiving task state.  See
        :class:`~celery.backend.base.BaseBackend`."""
        return self._get_backend()

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
                
                __subtasks__ = []
                
                class __metaclass__(TaskType):
                    def __init__(cls, name, bases, ns):
                        if name != 'PecanTask':
                            cls.__subtasks__.append(cls)
                        TaskType.__init__(cls, name, bases, ns)

                @property
                def backend(self):
                    return self.app.backend
        
            self.__task__ = PecanTask
            
        return self.__task__
        
base_app = BaseAppFactory().instance

# Exposed
PecanTaskFactory = BaseClassFactory()
task = base_app.task
conf = base_app.conf
