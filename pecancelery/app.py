from celery import app

__all__ = ['PecanTaskFactory']

class PecanCeleryApp(app.App):
    
    @property
    def conf(self):
        """Current configuration (dict and attribute access)."""
        return self._get_config()

class BaseClassFactory(object):
    
    __task__ = None
    
    @property
    def instance(self):
        if self.__task__ is None:
            self.__task__ = PecanCeleryApp(loader='pecancelery.loader.PecanLoader').create_task_cls()
        return self.__task__
        
PecanTaskFactory = BaseClassFactory()