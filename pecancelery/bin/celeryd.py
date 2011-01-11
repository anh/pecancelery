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
    
    def parse_config(self):
        self.config = self.load_configuration(self.args[0])
    
    def command(self): 
        self.parse_config()
               
        # get daemonize configuration
        # note that it should be under "conf.celery.__daemonize__"
        self.daemonize = self.config.celery.get('__daemonize__', False) is True
        
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
        
        pecancelery.app.base_app.Worker(queues = self.determine_queues()).run()

    def determine_queues(self):
        #
        # Look at all imported subclasses of pecancelery.Task
        # and compile a list of queues.
        #
        _all_queues = set(['default'])
        for sc in pecancelery.Task.__subclasses__:
            queue = getattr(sc, 'queue', None)
            if queue:
                _all_queues.add(queue)
        _all_queues = list(_all_queues)
        
        #
        # Determine the list of queues to process.  Default to
        # pecan.conf.celery['CELERYD_QUEUES'], and fall back to
        # the list of queues compiled above.
        #
        conf = getattr(self.config, 'celery', None)
        
        if conf and (getattr(conf, 'CELERYD_QUEUES', None) or conf.get('CELERYD_QUEUES')):
            return getattr(conf, 'CELERYD_QUEUES', conf['CELERYD_QUEUES'])
            
        return ','.join(_all_queues)

    def log_break(self):
        self.log('-' * 60)

    def log(self, message, type='log'):
        message = message.encode('ascii', 'replace')
        try:
            print '%s %s' % (datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'), message)
        except:
            print 'Error logging message!'        