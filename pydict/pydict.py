import sys
import abc
import json
import numbers
import logging
import logging.config
from abc import ABC
from persistence import XmlDictMdlPersistence
from view import PyDictAppView, PyDictGuiBuilder
from dictmdl import WordListModel
from PyQt5.QtWidgets import QApplication


logging.basicConfig()
with open('logging.json', 'r') as fd:
    logging.config.dictConfig(json.load(fd))
logger = logging.getLogger('pydict')



class PyDictApp(object):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._qapp = None
 

    def main(self) -> None:
        logger.error('Hello error world!')
        dmp = XmlDictMdlPersistence()
        dmp.path = 'dict.xml'
        dmp.load_dict()
        print(dmp.to_string())

        self._qapp = QApplication(sys.argv)

        guibldr = PyDictGuiBuilder()
        guibldr.title = 'PyDict'
        guibldr.dictmdl = dmp.dictmdl
        guibldr.qapp = self._qapp

        self._appview = guibldr.build()
        self._appview.show()
        sys.exit(self._qapp.exec_())




        

if __name__ == '__main__':
    app = PyDictApp()
    app.main()