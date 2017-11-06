import abc
from abc import ABC

class LangObj(ABC):
    """description of class"""

    @property
    def guid(self) -> int:
        return self._guid

    @guid.setter
    def guid(self, value: int) -> None:
        if not ( (value is None) or isinstance(value, int) ):
            raise TypeError('The guid property of {} shall have {} type.'
                            .format(self.__class__.__name__, int.__name__))
        self._guid = value

    @abc.abstractmethod
    def update(self, other: 'LangObj') -> None:
        pass
