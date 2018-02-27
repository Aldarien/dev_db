import logging

class LevelFilter(logging.Filter):
    def __init__(self, low, high=None):
        self._low = low
        if high:
            self._high = high
        else:
            self._high = low
        
        logging.Filter.__init__(self)
    def filter(self, record):
        if self._low <= record.levelno <= self._high:
            return True
        return False