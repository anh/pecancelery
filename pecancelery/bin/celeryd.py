from pecan.commands     import Command
from datetime           import datetime

import pecancelery
import os
import sys

class CeleryCommand(Command):
    """
    Spawn a celeryd worker instance.
    """
    
    # command information
    usage = 'CONFIG_NAME'
    summary = __doc__.strip().splitlines()[0].rstrip('.')
    
    # command options/arguments
    min_args = 1
    max_args = 1
    
    def command(self):        
        # load the application
        config = self.load_configuration(self.args[0])

        # get daemonize configuration
        # note that it should be under "conf.celery.__daemonize__"
        self.daemonize = config.celery.get('__daemonize__', False) is True
        
        # daemonize and detach from terminal by forking twice
        if self.daemonize:
            try:
                if os.fork() > 0:
                    sys.exit(0) # parent
            except OSError:
                sys.exit(1) # fork failed
        
            os.setsid()
            os.umask(0)
        
            try:
                pid = os.fork()
                if pid > 0:
                    sys.exit(0) # parent
            except OSError:
                sys.exit(1) # fork failed

        self.log_break()
        self.log('Starting celeryd...')

        _all_queues = ['default']
        # for sc in ShootQTask.subclasses:
        #     queue = getattr(sc, 'queue', None)
        #     if queue:
        #         _all_queues.append(queue)
        pecancelery.app.base_app.Worker().run()

    def log_break(self):
        self.log('-' * 60)

    def log(self, message, type='log'):
        message = message.encode('ascii', 'replace')
        try:
            print '%s %s' % (datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'), message)
        except:
            print 'Error logging message!'        