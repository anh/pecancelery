from pecancelery import Task, task

class ReverseTask(Task):
    
    queue = 'strings'
    
    def run(self, string, **kw):
        return string[::-1]