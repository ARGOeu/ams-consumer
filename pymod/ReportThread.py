import threading, time

from datetime import datetime, timedelta
from ams_consumer.SharedSingleton import SharedSingleton

class ReportThread(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self, name='stat_report_thread')

    def run(self):
        singleton = SharedSingleton()
        while True:
            hour24 = singleton.getLastStatTime() + timedelta(days = 1)
            if(datetime.now() > hour24):
                singleton.getLog().info(singleton.getLastStatTime().strftime('Since %Y-%m-%d %H:%M:%S messages consumed: %i') %
                     singleton.getMsgConsumed())
                singleton.resetCounters()

            if(singleton.getEventSigTerm().isSet()):
                singleton.getLog().info(singleton.getLastStatTime().strftime('Since %Y-%m-%d %H:%M:%S messages consumed: %i') %
                     singleton.getMsgConsumed())
                break

            if(singleton.getEventSigUsr1().isSet()):
                singleton.getLog().info(singleton.getLastStatTime().strftime('Since %Y-%m-%d %H:%M:%S messages consumed: %i') %
                     singleton.getMsgConsumed())
                singleton.resetCounters()
                singleton.getEventSigUsr1().clear()

            #singleton.getLog().info('tredovaca ljuta')
            time.sleep(1)


