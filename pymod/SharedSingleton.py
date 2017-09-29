class SharedSingleton(object):
    """
        Singleton object used to store configuration options and
        logger that need to be shared throughout the code
    """
    _sharedObj = None

    def __new__(cls, *args, **kwargs):
        if not getattr(cls, '_sharedObj', False):
            setattr(cls, '_sharedObj', object.__new__(cls))
        return cls._sharedObj

    def __init__(self, config, logger):
        if not getattr(self.__class__, '_config', False):
            self._config = config
        if not getattr(self.__class__, '_logger', False):
            self._logger = logger

    def getLog(self):
        return self._logger.get()

    def getConfig(self):
        return self._config

