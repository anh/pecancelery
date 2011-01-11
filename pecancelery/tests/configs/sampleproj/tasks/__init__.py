from pecancelery import Task, task

class AddTask(Task):
    
    queue = 'math'
    
    def run(self, x, y, **kw):
        return x + y
        
@task(queue='strings')
def concat(pre, post):
    return '%s%s' % (pre, post)