import os
import time
import codecs
import fcntl
from logging import Handler
from logging.handlers import TimedRotatingFileHandler


class MultiProcessSafeHandler(TimedRotatingFileHandler):
    def __init__(self, filename, when='h', interval=1, backupCount=0, encoding=None, utc=False):
        TimedRotatingFileHandler.__init__(self, filename, when, interval, backupCount, encoding, True, utc)
        self.current_file_name = self.get_new_file_name()
        self.lock_file = None

    def get_new_file_name(self):
        return self.baseFilename + "." + time.strftime(self.suffix, time.localtime()) + ".log"

    def shouldRollover(self, record):
        if self.current_file_name != self.get_new_file_name():
            return True
        return False

    def doRollover(self):
        if self.stream:
            self.stream.close()
            self.stream = None
        self.current_file_name = self.get_new_file_name()
        if self.backupCount > 0:
            for s in self.getFilesToDelete():
                os.remove(s)

    def _open(self):
        if self.encoding is None:
            stream = open(self.current_file_name, self.mode)
        else:
            stream = codecs.open(self.current_file_name, self.mode, self.encoding)
        return stream

    def acquire(self):
        self.lock_file = open(self.baseFilename + ".lock", "w")
        fcntl.lockf(self.lock_file, fcntl.LOCK_EX)

    def release(self):
        if self.lock_file:
            self.lock_file.close()
            self.lock_file = None
