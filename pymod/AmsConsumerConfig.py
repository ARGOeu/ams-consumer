import ConfigParser, os, re, ast

#import ipdb

class AmsConsumerConfig:

    GENERAL = 'General'
    AMS = 'AMS'
    MSG_RETENTION = 'MsgRetention'
    OUTPUT = 'Output'

    def __init__(self, configFile):
        self._filename = configFile
        self._options = {}


    def parse(self):
        config = ConfigParser.ConfigParser()
        if not os.path.exists(self._filename):
            #self.logger.error('Could not find %s' % self._filename)
            raise SystemExit(1)
        config.read(self._filename)

        for section in config.sections():
            key = section.lower()
            self._options[key] = {}
            for option, value in config.items(section):
                new_value = self._getCorrectOptionValueType(value)
                self._options[key].update({option: new_value})

       #ipdb.set_trace()

    def getOption(self, section, option):
        return self.getSection(section)[option.lower()]

    def getSection(self, section):
        return self._options[section.lower()]

    def _getCorrectOptionValueType(self, value):
        if re.match("^\d+$", value):
            return int(value)
        elif value == 'True' or value == 'False':
            return ast.literal_eval(value)
        elif re.search(",| ", value):
            orig_array = filter(None, re.split(",| ", value))
            new_array = []
            for elem in orig_array:
                new_array.append(self._getCorrectOptionValueType(elem))
            return new_array
        else:
            return value


