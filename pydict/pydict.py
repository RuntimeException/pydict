import abc
import json
import numbers
import logging
import logging.config
from abc import ABC
from language.word import Word
from lxml import etree
from persistence import XmlDictMdlPersistence


logging.basicConfig()
with open('logging.json', 'r') as fd:
    logging.config.dictConfig(json.load(fd))
logger = logging.getLogger('pydict')



class PyDictApp(object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def main(self) -> None:
        logger.error('Hello error world!')
        dmp = XmlDictMdlPersistence()
        dmp.path = 'dict.xml'
        dmp.load_dict()
        print(dmp.to_string())
        pass

        
        

if __name__ == '__main__':
    app = PyDictApp()
    app.main()