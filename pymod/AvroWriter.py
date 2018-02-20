import os
import avro.schema

from avro.datafile import DataFileWriter
from avro.io import DatumWriter, BinaryEncoder, BinaryDecoder, DatumReader
from ams_consumer.SharedSingleton import SharedSingleton
from ams_consumer.AmsConsumerConfig import AmsConsumerConfig
from io import BytesIO
from datetime import datetime, timedelta

class AvroWriter:

    _filename = None
    _errorFile = None
    _schema = None
    _config = None
    _avroFile = None


    def __init__(self):
        self._shared = SharedSingleton()
        self._config = self._shared.getConfig()
        self._log = self._shared.getLog()
        self._filename = (self._config.getOption(AmsConsumerConfig.OUTPUT, 'Directory') + '/' +
                        self._config.getOption(AmsConsumerConfig.OUTPUT, 'Filename'))

        self._errorFile = (self._config.getOption(AmsConsumerConfig.OUTPUT, 'Directory') + '/' +
                        self._config.getOption(AmsConsumerConfig.OUTPUT, 'ErrorFilename'))

        self.loadSchema(self._config.getOption(AmsConsumerConfig.GENERAL, 'AvroSchema'))


    def processMessages(self, msgList):
        for msgDate, msgPayloads in msgList.iteritems():
            fileWriter = self.getFileWriter(msgDate)
            for msg in msgPayloads:
                msgContent = self.deserialize(msg)
                fileWriter.append(msgContent)

            fileWriter.close()
            self._avroFile.close()


    def loadSchema(self, schemaFile):
        try:
            f = open(schemaFile)
            self._schema = avro.schema.parse(f.read())
        except Exception as e:
            self._log.error(e)
            raise SystemExit(1)


    def deserialize(self, message):
        avro_reader = DatumReader(self._schema)
        bytesio = BytesIO(message)
        decoder = BinaryDecoder(bytesio)
        return avro_reader.read(decoder)


    def getFileWriter(self, datum):
        msgDate = datetime.strptime(datum, '%Y-%m-%d')
        today = datetime.today()

        if(msgDate + timedelta(days=self._config.getOption(AmsConsumerConfig.MSG_RETENTION, 'PastDaysOk')) > today
           and msgDate - timedelta(days=self._config.getOption(AmsConsumerConfig.MSG_RETENTION, 'FutureDaysOk')) < today):
            avroFilename = self._filename.replace('DATE', datum)
        else:
            avroFilename = self._errorFile.replace('DATE', datum)

        if os.path.exists(avroFilename):
            self._avroFile = open(avroFilename, 'a+')
            writer = DataFileWriter(self._avroFile, DatumWriter())
        else:
            self._avroFile = open(avroFilename, 'w+')
            writer = DataFileWriter(self._avroFile, DatumWriter(), self._schema)

        return writer
