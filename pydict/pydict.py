import abc
import json
import numbers
import logging
import logging.config
from abc import ABC
from xml.etree import ElementTree
from language.word import Word


logging.basicConfig()
with open('logging.json', 'r') as fd:
    logging.config.dictConfig(json.load(fd))
logger = logging.getLogger('pydict')


class IPyDictModel(ABC):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @abc.abstractmethod
    def add_word(self, word: Word) -> None:
        pass

    @abc.abstractmethod
    def get_word(self, guid: int) -> Word:
        pass

    
class PyDictModelMap(IPyDictModel):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._wordlist = []

    def add_word(self, word: Word) -> None:
        if not isinstance(word, Word):
            raise TypeError('The word parameter of {} method in {} class shall have {} type.'
                            .format(add_word.__name__, self.__class__.__name__, Word.__name__))
    
    
    

class PyDictApp(object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)




    def main(self) -> None:
        logger.error('Hello error world!')

if __name__ == '__main__':
    app = PyDictApp()
    app.main()
    
    print('Hello world!')