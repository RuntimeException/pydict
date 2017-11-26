from enum import Enum, IntEnum, unique
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
            cls.handlers.remove(handler)
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


class Event(ABC):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.handlers = []

    @abc.abstractmethod
    def eventid(self) -> 'EventId':
        pass


class EventSaveAll(Event):

    def eventid(self) -> 'EventId':
        return EventId.SAVE_ALL


@unique
class EventId(Enum):
    INVALID  = (0, Event)
    SAVE_ALL = (1, EventSaveAll)

    def __init__(self, id: int, eventclass: type):
        self.id = id
        self.eventclass = eventclass

    def create_event(self, **kwargs):
        return self.eventclass(**kwargs)


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


    def fire(self, event: Event = None) -> Event:
        if event is None:
            event = self.eventid.create_event()
        else:
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