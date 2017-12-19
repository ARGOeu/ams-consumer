import threading, time

from datetime import datetime, timedelta
from ams_consumer.SharedSingleton import SharedSingleton

class ReportThread:
    _thread = None

    def __init__(self):
        self._thread = threading.Thread(target=self.run, name='stat_report_thread')

    def start(self):
        self._thread.start()

    def run(self):
        import ipdb
  #      ipdb.set_trace()

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
            #ipdb.set_trace()
            if(singleton.getEventSigUsr1().isSet()):
                singleton.getLog().info(singleton.getLastStatTime().strftime('Since %Y-%m-%d %H:%M:%S messages consumed: %i') %
                     singleton.getMsgConsumed())
                singleton.resetCounters()
                singleton.getEventSigUsr1().clear()

            singleton.getLog().info('tredovaca ljuta')
            time.sleep(1)


