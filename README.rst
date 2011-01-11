===============================================
 pecancelery - Celery Integration for the Pecan web framework
===============================================

--

pecancelery provides Celery integration for the `Pecan`_ framework.

`Celery`_ is a task queue/job queue based on distributed message passing.
It is focused on real-time operation, but supports scheduling as well.

The execution units, called tasks, are executed concurrently on a single or
more worker servers. Tasks can execute asynchronously (in the background) or
synchronously (wait until ready).

Celery is already used in production to process millions of tasks a day.

Celery is written in Python, but the protocol can be implemented in any
language. It can also `operate with other languages using webhooks`_.

The recommended message broker is `RabbitMQ`_, but support for `Redis`_ and
databases (via `SQLAlchemy`) is also available.

.. _`Celery`: http://celeryproject.org/
.. _`Pecan`: http://www.pecanpy.org/
.. _`RabbitMQ`: http://www.rabbitmq.com/
.. _`Redis`: http://code.google.com/p/redis/
.. _`SQLAlchemy`: http://www.sqlalchemy.org/
.. _`operate with other languages using webhooks`:
    http://ask.github.com/celery/userguide/remote-tasks.html

.. contents::
    :local:

Enabling pecancelery
------------------------------

To enable ``pecancelery`` for your project you need to add the following line
to the top of your configuration file(s) (e.g., ``config.py``)::

    import pecancelery
    
Also, in your project's setup.py, you should add ``pecancelery`` into ``paster_plugins``.

::

  setup(
    name                    = 'SuperBlog',
    version                 = '0.1',
    ...
    paster_plugins = ['pecan', 'pecancelery'],
    ...
  )
  
Configuring pecancelery
------------------------------

Your pecan configuration file(s) may include a ``celery`` block:

::

  # Pecan Application Configurations
  app = {
      'root' : RootController,
      ...
  }

  # Celery Configuration
  celery = {
    'BROKER_HOST'                           : 'localhost',
    'BROKER_PORT'                           : 5672,
    'BROKER_USER'                           : 'username',
    'BROKER_PASSWORD'                       : 'password',
    'BROKER_VHOST'                          : 'vhost',
    'CELERY_RESULT_BACKEND'                 : 'database',
    'CELERY_RESULT_DBURI'                   : 'mysql://root:password@localhost/dbname?charset=utf8&use_unicode=0',
    'CELERYD_LOG_LEVEL'                     : 'DEBUG'
  }

Configuration options are documented at http://celeryq.org/docs/configuration.html.
  
Defining and queueing tasks with pecancelery
------------------------------
    
In your pecan project root (where your controllers and template folder live), you should define a ``tasks`` module
that contains implementations of ``pecancelery.Task`` and/or functions decorated with ``pecancelery.task``:

::

  from pecancelery import Task, task
  
  @task()
  def add(x, y): 
      return x + y
  
  class AddTask(Task):
    def run(self, x, y, **kw):
      return x + y
      
From any pecan app controller, you can queue tasks just like you do with celery:

::

  from superblog.tasks import AddTask

  class SampleController(object):

    @expose()
    def index(self):
      AddTask.delay(2, 2)
      
To start a celeryd worker, just use the `pecan` command:

::

  user$ pecan celeryd config.py
  
Routing tasks to queues
------------------------------

When defining tasks, you can specify a queue they should be routed to:

::

  class AddTask(Task):
    
      queue = 'math'
    
      def run(self, x, y, **kw):
          return x + y
        
  @task(queue='strings')
  def concat(pre, post):
      return '%s%s' % (pre, post)
      
By default, pecancelery will auto-discover your defined queues and bind workers to all of them.
If you'd like to override this behavior, just specify ``CELERYD_QUEUES`` in your pecan config file(s):

::

  # Celery Configuration
  celery = {
    'BROKER_HOST'                           : 'localhost',
    'BROKER_PORT'                           : 5672,
    ...
    'CELERYD_QUEUES'                        : 'math,other',
  }

Using the development version
------------------------------

You can clone the git repository by doing the following::

    $ git clone git://github.com/ryanpetrello/pecancelery.git
