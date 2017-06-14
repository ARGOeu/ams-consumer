#!/usr/bin/python

import sys, os, hashlib, time, syslog
import daemon
import daemon.pidlockfile
import argparse
import signal
import errno

import ipdb

pid_dir = '/var/run/'
log_file = '/tmp/fajla'


def doMainProgram(fh):
  #  fh = open(log_file, 'a')
    while True:
        time.sleep(5)
        syslog.syslog("vrti se demon" )
        fh.write("u fajli se vrti..")


def startDaemon(context_daemon):
    if context_daemon.pidfile.is_locked and not context_daemon.pidfile.i_am_locking():
        pid = context_daemon.pidfile.read_pid()
        if pid:
            try:
                os.kill(int(pid), 0)
                return 1
            except OSError, e:
                # no such process
                if(e.errno == errno.ESRCH):
                    context_daemon.pidfile.break_lock()

    fh = open(log_file, 'a')
    fh.write("inicijalizacija\n")
    context_daemon.files_preserve = [fh]

    def sigusrhandle(signum, frame):
        syslog.syslog("sigusr1 ufacen.." + fh.name + "--\n")
        fh.write("SIG1 uvacen\n")
        fh.flush()
       # return 0

    context_daemon.signal_map = {
        signal.SIGUSR1: sigusrhandle,
        signal.SIGTERM: 'terminate'
    }

    with context_daemon:
        doMainProgram(fh)


def stopDaemon(context_daemon):
    if context_daemon.pidfile.is_locked():
        pid = context_daemon.pidfile.read_pid()
        try:
            os.kill(pid, signal.SIGTERM)
        except OSError, e:
            if(e.errno == errno.ESRCH):
                context_daemon.pidfile.break_lock()

    return 0


def calcPidName(config_file):
    if not os.path.isfile(config_file):
        raise SystemExit(2)
    fh = open(config_file, 'r')
    hash_obj = hashlib.md5(fh.read())   #ipdb.set_trace()
    fh.close()
    pid_name = 'amsconsd_' + hash_obj.hexdigest()[0:8] + '.pid'

    return pid_name


def daemonize(args):
    pid_fullname = pid_dir + calcPidName(args.config)

    context_daemon = daemon.DaemonContext()
    context_daemon.pidfile = daemon.pidlockfile.PIDLockFile(pid_fullname, threaded=False)

    if args.daemon == 'start':
        startDaemon(context_daemon)
    elif args.daemon == 'stop':
        ret = stopDaemon(context_daemon)
        raise SystemExit(ret)


def main():
    parser = argparse.ArgumentParser(prog='ams-consumerd')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-n', dest='nofork', action='store_true',
                        help='do not fork into background')
    group.add_argument('-d', dest='daemon', type=str,
                       help='daemon arguments: start, stop, restart, status', metavar='')
    parser.add_argument('-c', dest='config', type=str, required=True, help='config file')
    args = parser.parse_args()

    if args.nofork:
        try:
            print 'ne forkam'
            #init_dirq_consume(shared.workers, daemonized=False)
        except KeyboardInterrupt:
            raise SystemExit(1)

    elif args.daemon:
        daemonize(args)

if __name__ == "__main__":
    main()
