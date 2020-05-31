from enum import Enum, IntEnum, unique
import abc
from abc import ABC
from language.word import Word
import numbers
import logging

logger = logging.getLogger(__name__)

@unique
class EventId(IntEnum):
    EVENT = 0
    EVENT_SAVE_ALL= 1
    EVENT_WORD_ADD_REQ = 2
    EVENT_WORD_REMOVE_REQ = 3
    EVENT_WORD_UPDATE_REQ = 4
    EVENT_WORD_ADDED = 5
    EVENT_WORD_REMOVED = 6
    EVENT_WORD_UPDATED = 7


class Event(ABC):
    handlers = {}
    string_detailed = False

    @classmethod
    def eventid(cls) -> EventId:
        return EventId.EVENT

    @classmethod
    def subscribe(cls, handler: object) -> None:
        if callable(handler):
            logger.info('The {} is subscribed to the {} event.'
                        .format(str(handler), cls.eventid().name))
            eid = cls.eventid()
            if eid not in cls.handlers:
                cls.handlers[eid] = [handler]
            else:
                cls.handlers[eid].append(handler)           
        else:
            raise TypeError('Event handler shall be callable but {} is not callable.'
                            .format(str(handler)))

    @classmethod
    def unsubscribe(cls, handler: object) -> None:
        if callable(handler):
            eid = cls.eventid()
            if (eid in cls.handlers) and (handler in cls.handlers[id]):
                cls.handlers[id].remove(handler)
                logger.info('The {} is unsubscribed to the {} event.'
                            .format(str(handler), cls.eventid().name))
            else:
                pass # Maybe logging later
        else:
            raise TypeError('Event handler shall be callable but {} is not callable.'
                            .format(str(handler)))

    def __init__(self, **kwargs):
        raise NotImplementedError('Event shall not instantiated because it is an abstract class.')


    def fire(self, *args, **kwargs) -> None:
        base_event_processed = False
        cls = self.__class__
        eid = cls.eventid()
        while not base_event_processed:
            if eid in self.handlers:
                for handler in self.handlers[eid]:
                    handler(self, *args, **kwargs)
            if cls.eventid() != EventId.EVENT:
                cls = cls.__bases__[0]
                eid = cls.eventid()
            else:
                base_event_processed = True

    def __str__(self) -> str:
        return '{}{{}}'.format(self.eventid().name)



class EventSaveAll(Event):

    def __init__(self, **kwargs):
        pass

    @classmethod
    def eventid(cls) -> EventId:
        return EventId.EVENT_SAVE_ALL



class EventWordAddRequest(Event): 

    @classmethod
    def eventid(cls) -> EventId:
        return EventId.EVENT_WORD_ADD_REQ

    def __init__(self, word: Word, **kwargs):
        self.word = word

    @property
    def word(self) -> Word:
        return self._word

    @word.setter
    def word(self, value: Word) -> None:
        assert ( (value is None) or isinstance(value, Word) ),\
                'The word property of {} shall have {} type.'\
                .format(self.__class__.__name__, Word.__name__)
        self._word = value

    def __str__(self):
        return '{}{{{}, {}}}'.format(self.eventid().name, self.super)



class EventWordRemoveRequest(Event):

    @classmethod
    def eventid(cls) -> EventId:
        return EventId.EVENT_WORD_REMOVE_REQ
    
    def __init__(self, guid: int, **kwargs):
        self.guid = guid

    @property
    def guid(self) -> int:
        return self._guid

    @guid.setter
    def guid(self, value: int) -> None:
        assert ( (value is None) or isinstance(value, int) ),\
                'The guid property of {} shall have {} type.'\
                .format(self.__class__.__name__, int.__name__)
        self._guid = value



class EventWordUpdateRequest(Event):

    @classmethod
    def eventid(cls) -> EventId:
        return EventId.EVENT_WORD_UPDATE_REQ
    
    def __init__(self, word: Word, **kwargs):
        self.word = word

    @property
    def word(self) -> Word:
        return self._word

    @word.setter
    def word(self, value: Word) -> None:
        assert ( (value is None) or isinstance(value, Word) ),\
                'The word property of {} shall have {} type.'\
                .format(self.__class__.__name__, Word.__name__)
        self._word = value



class EventWordAdded(Event):

    @classmethod
    def eventid(cls) -> EventId:
        return EventId.EVENT_WORD_ADDED
    
    def __init__(self, guid: int, **kwargs):
        self.guid = guid

    @property
    def guid(self) -> int:
        return self._guid

    @guid.setter
    def guid(self, value: int) -> None:
        assert ( (value is None) or isinstance(value, int) ),\
                'The guid property of {} shall have {} type.'\
                .format(self.__class__.__name__, int.__name__)
        self._guid = value



class EventWordRemoved(Event):

    @classmethod
    def eventid(cls) -> EventId:
        return EventId.EVENT_WORD_REMOVED
    
    def __init__(self, guid: int, **kwargs):
        self.guid = guid

    @property
    def guid(self) -> int:
        return self._guid

    @guid.setter
    def guid(self, value: int) -> None:
        assert ( (value is None) or isinstance(value, int) ),\
                'The guid property of {} shall have {} type.'\
                .format(self.__class__.__name__, int.__name__)
        self._guid = value



class EventWordUpdated(Event):

    @classmethod
    def eventid(cls) -> EventId:
        return EventId.EVENT_WORD_UPDATED
    
    def __init__(self, guid: int, **kwargs):
        self.guid = guid

    @property
    def guid(self) -> int:
        return self._guid

    @guid.setter
    def guid(self, value: int) -> None:
        assert ( (value is None) or isinstance(value, int) ),\
                'The guid property of {} shall have {} type.'\
                .format(self.__class__.__name__, int.__name__)
        self._guid = value



class EventSource(object):

    def __init__(self, eventid: EventId, **kwargs):
        super().__init__(**kwargs)
        self.eventid = eventid
        self._handlers = []

    @property
    def eventid(self) -> EventId:
        return self._eventid

    @eventid.setter
    def eventid(self, value: EventId) -> None:
        assert isinstance(value, EventId), 'The eventid property of {} class shall have {} type.'\
               .format(self.__class__.__name__, EventId.__name__)
        self._eventid = value


    def subscribe(self, handler: object) -> None:
        if callable(handler):
            self._handlers.append(handler)
        else:
            raise TypeError('Event handler shall be callable but {} is not callable.'
                            .format(str(handler)))


    def unsubscribe(self, handler: object) -> None:
        if callable(handler):
            self._handlers.remove(handler)
        else:
            raise TypeError('Event handler shall be callable but {} is not callable.'
                            .format(str(handler)))


    def fire(self, event: Event) -> Event:
        if event.eventid() != self.eventid:
            raise TypeError('The expected eventid of {} is {} but {} was passed.'
                            .format(self.__class__.__name__, self.eventid.name, event.eventid.name))

        for handler in self._handlers:
            handler(event)
        return event



class EventBus(object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._eventsrcs = []
        self._routing_table = {}


    def add_eventsrc(self, eventsrc: EventSource) -> None:
        assert isinstance(eventsrc, EventSource), 'The eventsrc parameter of {} method in {} class shall have {} type.'\
               .format(add_event_src.__name__, self.__class__.__name__, EventSource.__name__)
        self._eventsrcs.append(eventsrc)
        eventsrc.subscribe(self.route_event)


    def remove_eventsrc(self, eventsrc: EventSource) -> None:
        assert isinstance(eventsrc, EventSource), 'The eventsrc parameter of {} method in {} class shall have {} type.'\
               .format(remove_event_src.__name__, self.__class__.__name__, EventSource.__name__)
        self._eventsrcs.remove(eventsrc)
        eventsrc.unsubscribe(self.route_event)


    def subscribe(self, eventid: EventId, handler: object) -> None:
        assert isinstance(eventid, EventId), 'The eventid parameter of {} method in {} class shall have {} type.'\
                                             .format(subscribe.__name__, self.__class__.__name__, EventId.__name__)
        if callable(handler):
            if eventid not in self._routing_table:
                self._routing_table[eventid] = [handler]
            else:
                self._routing_table[eventid].append(handler)
        else:
            raise TypeError('Event handler shall be callable but {} is not callable.'
                            .format(str(handler)))


    def unsubscribe(self, eventid: EventId, handler: object) -> None:
        assert isinstance(eventid, EventId), 'The eventid parameter of {} method in {} class shall have {} type.'\
                                             .format(unsubscribe.__name__, self.__class__.__name__, EventId.__name__)
        if callable(handler):
            if eventid not in self._routing_table:
                self._routing_table[eventid].remove(handler)
        else:
            raise TypeError('Event handler shall be callable but {} is not callable.'
                            .format(str(handler)))


    def route_event(self, event: Event) -> Event:
        if event.eventid() in self._routing_table:
            for handler in self._routing_table[event.eventid()]:
                handler(event)
        return event