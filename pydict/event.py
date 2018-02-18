from enum import Enum, IntEnum, unique
import abc
from abc import ABC
 

@unique
class EventId(IntEnum):
    EVENT = 0
    EVENT_SAVE_ALL= 1


class Event(ABC):
    handlers = {}

    @classmethod
    def eventid(cls) -> EventId:
        return EventId.EVENT

    @classmethod
    def subscribe(cls, handler: object) -> None:
        if callable(handler):
            eid = cls.eventid()
            if eid not in cls.handlers:
                handlers[eid] = [handler]
            else:
                handlers[eid].append(handler)           
        else:
            raise TypeError('Event handler shall be callable but {} is not callable.'
                            .format(str(handler)))

    @classmethod
    def unsubscribe(cls, handler: object) -> None:
        if callable(handler):
            eid = cls.eventid()
            if (eid in cls.handlers) and (handler in cls.handlers[id]):
                cls.handlers[id].remove(handler)
            else:
                pass # Maybe logging later
        else:
            raise TypeError('Event handler shall be callable but {} is not callable.'
                            .format(str(handler)))

    def __init__(self, **kwargs):
        raise NotImplementedError('Event shall not instantiated because it is an abstract class.')


    def fire(self, **kwargs):
        eid = cls.eventid()
        if eid in cls.handlers:
            for handler in self.handlers[eid]:
                handler(self, **kwargs)
        super().fire()
            

    def __str__(self) -> str:
        return '{}{}'.format(self.eventid.name, self.__dict__)


class EventSaveAll(Event):

    def eventid(self) -> EventId:
        return EventId.EVENT_SAVE_ALL


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