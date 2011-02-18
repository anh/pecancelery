from pecan.commands.base    import Command
from socket                 import gethostname
from datetime               import datetime

class CeleryCommand(Command):
    """
    Broadcast a kill message to celery workers
    """
    
    # command information
    usage = 'CONFIG_NAME'
    summary = __doc__.strip().splitlines()[0].rstrip('.')
    
    # command options/arguments
    min_args = 1
    max_args = 1
    
    parser = Command.standard_parser(verbose=True)
    parser.add_option('--hosts',
        dest='hosts',
        help='Prevents the daemon from detaching/daemonizing.')
    
    def parse_config(self):
        self.config = self.load_configuration(self.args[0])
    
    def command(self): 
        from celery.task.control import broadcast
        self.parse_config()

        self.log_break()
        self.log('Starting celerystop...')
        
        #
        # Look for hosts to broadcast to in the command line arguments,
        # e.g.,
        # pecan celerystop config.py --hosts=8.17.172.226,8.17.12.225
        # If no arguments are found, defaults to the hostname of the executing machine.
        #
        
        hosts = []
        args = self.options.hosts
        if args:
            hosts = args.split(',')
        else:
            hosts = [gethostname()]
            
        broadcast('shutdown', destination=hosts)

    def log_break(self):
        self.log('-' * 60)

    def log(self, message, type='log'):
        message = message.encode('ascii', 'replace')
        try:
            print '%s %s' % (datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'), message)
        except:
            print 'Error logging message!'