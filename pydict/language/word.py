from language.langobj import LangObj
from enum import Enum, unique
import abc

@unique
class WordClass(Enum):
    NOUN = 0
    VERB = 1

class Word(LangObj):
    """description of class"""

    @abc.abstractmethod
    def get_wordclass(self):
        pass
        