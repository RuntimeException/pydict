from enum import IntEnum, unique
import abc
from abc import ABC

class GlobalEventManager(object):

    pass


@unique
class GlobalEventId(IntEnum):
    INVALID = 0
    DICT_MODIFIED = 1
    

class GlobalEvent(ABC):
    handlers = []

    @classmethod
    def eventid(cls) -> GlobalEventId:
        return GlobalEventId.INVALID

    @classmethod
    def subscribe(cls, handler: object) -> None:
        if callable(handler):
            cls.handlers.append(handler)
        else:
            raise TypeError('Event handler shall be callable but {} is not callable.'
                            .format(str(handler)))

    @classmethod
    def unsubscribe(cls, handler: object) -> None:
        if callable(handler):
            cls.handlers.append(handler)
        else:
            raise TypeError('Event handler shall be callable but {} is not callable.'
                            .format(str(handler)))

    def __init__(self, **kwargs):
        pass


    def fire(self, **kwargs):
        for handler in self.handlers:
            handler(self, **kwargs)

    def __str__(self) -> str:
        return '{}{}'.format(self.eventid.name, self.__dict__)

class GlobalDictModEvent(GlobalEvent):
    handlers = []