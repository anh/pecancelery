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
databases (`SQLAlchemy`_ / `Django`_) is also available.

.. _`Celery`: http://celeryproject.org/
.. _`Pecan`: http://www.pecanpy.org/
.. _`RabbitMQ`: http://www.rabbitmq.com/
.. _`Redis`: http://code.google.com/p/redis/
.. _`Django`: http://www.djangoproject.org/
.. _`SQLAlchemy`: http://www.sqlalchemy.org/
.. _`operate with other languages using webhooks`:
    http://ask.github.com/celery/userguide/remote-tasks.html

.. contents::
    :local:

Using pecancelery
===================

To enable ``pecancelery`` for your project you need to add the following line
to the top of your configuration file(s) (e.g., ``config.py``)::

    import pecancelery
    
In your pecan project root (where your controllers and template folder live), you should define a ``tasks`` module
that contains implementations of ``pecancelery.Task` and/or functions decorated with pecancelery.task`:

::

  from pecancelery import Task, task
  
  @task()
  def add(x, y): 
      return x + y
  
  class AddTask(Task):
    def run(self, x, y, **kw):
      return x + y

Using the development version
------------------------------

You can clone the git repository by doing the following::

    $ git clone git://github.com/ryanpetrello/pecancelery.git
