from language.langobj import LangObj
from enum import Enum, unique
import abc

@unique
class WordClass(Enum):
    NOUN = 0
    VERB = 1

class Word(LangObj):
    """description of class"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._hun = set()

    @abc.abstractmethod
    def get_wordclass(self):
        pass
       
    @property
    def hun(self) -> set:
        return self._hun