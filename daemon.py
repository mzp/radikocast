import os
import sys

def daemonize(pidfile, daemonfunc, *args):
    try:
        pid = os.fork()
        if (pid > 0):
            sys.exit(0)
    except OSError:
        print >>sys.stderr, 'daemonize: fork #1 failed.'
        sys.exit(1)

    try:
        os.setsid()
    except:
        print >>sys.stderr, 'daemonize: setsid failed.'
        sys.exit(1)

    try:
        pid = os.fork()
        if (pid > 0):
            sys.exit(0)
    except OSError:
        print >>sys.stderr, 'daemonize: fork #2 failed.'
        sys.exit(1)

    try:
        f = file(pidfile, 'w')
        f.write('%d\n' % os.getpid())
        f.close()
    except IOError:
        print >>sys.stderr, 'daemonize: failed to write pid to %s' % pidfile
        sys.exit(1)

    # Now I'm a daemon.
    try:
#        os.chdir('/')
        os.umask(0)
        sys.stdin.close(); sys.stdin = None
        sys.stdout.close(); sys.stdout = None
        sys.stderr.close(); sys.stderr = None
        os.close(0)
        os.close(1)
        os.close(2)
    except:
        pass

    daemonfunc(*args)
