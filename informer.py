from enum import Enum

class Status(Enum):
    ERROR = 0b00
    WATING = 0b01
    IN_PROGRESS = 0b10
    DONE = 0b11

    
class Informer:

    _status:Status = Status.WATING
    _progress = 0

    _observers = []

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        if value == Status.DONE:
            self._progress = 100
        elif value == Status.ERROR or value == Status.WATING:
            self._progress = 0
        if self._status != value:
            self._status = value
            self.notify()

    @property
    def progress(self):
        return self._progress

    @progress.setter
    def progress(self, value):
        if value <0:
            value  = 0
        if value >100 :
            value = 100
        if value == 100:
            self.status = Status.DONE
        if value >0 and value < 100:
            self.status = Status.IN_PROGRESS
        if value ==0:
            self.status = Status.WATING
        if value != self._progress:
            self._progress = value
            self.notify()

    def watch(self, observer):
        if observer not in self._observers:
            self._observers.append(observer)
    
    def notify(self):
        for observer in self._observers:
            observer.update_progress(self)