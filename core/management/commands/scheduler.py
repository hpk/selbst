from django.core.management.base import NoArgsCommand
from django.conf import settings
from utils import call_func
from twisted.internet import reactor

class Command(NoArgsCommand):

    help = "Event handler for Selbst"

    def handle_noargs(self, **options):
        for d in settings.DAEMON_FNS:
            print "Starting daemon %s" % d
            call_func(d)
        reactor.run()

