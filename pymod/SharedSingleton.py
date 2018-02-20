from datetime import datetime
from threading import Event


class SharedSingleton(object):
    """
        Singleton object used to store configuration options and
        logger that need to be shared throughout the code
    """
    _sharedObj = None
    _msgConsumed = 0
    _lastStatTime = None
    _eventSigUsr1 = None
    _eventSigTerm = None

    def __new__(cls, *args, **kwargs):
        if not getattr(cls, '_sharedObj', False):
            setattr(cls, '_sharedObj', object.__new__(cls))
        return cls._sharedObj

    def __init__(self, config=None, logger=None):
        if config and logger:
            if not getattr(self, '_config', False):
                self._config = config
            if not getattr(self, '_logger', False):
                self._logger = logger
            self.resetCounters()
            self._eventSigUsr1 = Event()
            self._eventSigTerm = Event()

    def getLog(self):
        return self._logger.get()

    def getConfig(self):
        return self._config

    def incrementMsgCount(self):
        self._msgConsumed += 1

    def setLastStatTime(self, lst):
        self._lastStatTime = lst

    def getMsgConsumed(self):
        return self._msgConsumed

    def getLastStatTime(self):
        return self._lastStatTime

    def resetCounters(self):
        self._msgConsumed = 0
        self._lastStatTime = datetime.now()

    def getEventSigUsr1(self):
        return self._eventSigUsr1

    def getEventSigTerm(self):
        return self._eventSigTerm
