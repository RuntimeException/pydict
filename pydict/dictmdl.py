import abc
import numbers
from abc import ABC
from language.word import Word

class IDictModel(ABC):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @abc.abstractmethod
    def add_word(self, word: Word) -> None:
        pass

    @abc.abstractmethod
    def get_word(self, guid: int) -> Word:
        pass

    @abc.abstractmethod
    def __contains__(self, key: object) -> bool:
        pass

    @abc.abstractmethod
    def get_wordlist(self, is_ordered: bool = False, guid_asc_ndesc: bool = True) -> list:
        pass

    
class DictModelMap(IDictModel):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._worddict = {}


    def add_word(self, word: Word) -> None:
        assert isinstance(word, Word), 'The word parameter of {} method in {} class shall have {} type.'\
               .format(self.add_word.__name__, self.__class__.__name__, Word.__name__)
        self._worddict[word.guid] = word


    def get_word(self, guid: numbers.Integral) -> Word:
        assert isinstance(guid, numbers.Integral), 'The guid parameter of {} method in {} class shall have {} type.'\
               .format(self.get_word.__name__, self.__class__.__name__, numbers.Integral.__name__)
        return self._worddict.get(guid)


    def __contains__(self, key: object) -> bool:
        return key in self._worddict

    
    def get_wordlist(self, is_ordered: bool = False, guid_asc_ndesc: bool = True) -> list:
        wordlist = list(self._worddict.values())
        if is_ordered == True:
            if guid_asc_ndesc:
                wordlist.sort(key = lambda word: word.guid, reverse = False)
            else:
                wordlist.sort(key = lambda word: word.guid, reverse = True)
        return wordlist
        
        