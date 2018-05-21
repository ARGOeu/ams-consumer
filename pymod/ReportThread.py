import threading
import time

from decimal import Decimal
from datetime import datetime, timedelta
from argo_ams_consumer.SharedSingleton import SharedSingleton
from argo_ams_consumer.AmsConsumerConfig import AmsConsumerConfig


class ReportThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self, name='stat_report_thread')

    def run(self):
        singleton = SharedSingleton()
        while True:
            reportEveryHours = singleton.getConfig().getOption(AmsConsumerConfig.GENERAL, 'ReportWritMsgEveryHours')
            reportPeriod = singleton.getLastStatTime() + timedelta(hours=reportEveryHours)
            if(datetime.now() > reportPeriod):
                singleton.getLog().info('Consumed %i messages in %i hours' % (singleton.getMsgConsumed(), reportEveryHours))
                singleton.resetCounters()

            if(singleton.getEventSigTerm().isSet()):
                diff = datetime.now() - singleton.getLastStatTime()
                diff = Decimal(diff.seconds) / Decimal(3600)
                singleton.getLog().info('Consumed %i messages in %.3f hours' % (singleton.getMsgConsumed(), diff))
                break

            if(singleton.getEventSigUsr1().isSet()):
                diff = datetime.now() - singleton.getLastStatTime()
                diff = Decimal(diff.seconds) / Decimal(3600)
                singleton.getLog().info('Consumed %i messages in %.3f hours' % (singleton.getMsgConsumed(), diff))
                singleton.getEventSigUsr1().clear()

            time.sleep(1)
