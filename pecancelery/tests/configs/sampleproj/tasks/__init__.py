from pecancelery import Task, task

class AddTask(Task):
    def run(self, x, y, **kw):
        return x + y
        
@task()
def subtract(x, y):
    return x - y