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
from event import EventBus, EventId, Event


logging.basicConfig()
with open('logging.json', 'r') as fd:
    logging.config.dictConfig(json.load(fd))
logger = logging.getLogger('pydict')



class PyDictApp(object):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._qapp = None
        self._dictmdl = None
        self._eventbus = EventBus()
 

    def main(self) -> None:
        dmp = XmlDictMdlPersistence()
        dmp.path = 'dict.xml'
        dmp.load_dict()
        print(dmp.to_string())

        self._dictmdl = dmp.dictmdl
        self._qapp = QApplication(sys.argv)

        guibldr = PyDictGuiBuilder()
        guibldr.title = 'PyDict'
        guibldr.dictmdl = dmp.dictmdl
        guibldr.qapp = self._qapp
        guibldr.eventbus = self._eventbus

        self._appview = guibldr.build()
        self._appview.show()

        self._eventbus.subscribe(EventId.SAVE_ALL, self.handler_saveall)
        sys.exit(self._qapp.exec_())

    def handler_saveall(self, event: Event) -> None:
        dmp = XmlDictMdlPersistence()
        dmp.dictmdl = self._dictmdl
        dmp.path = 'dict.xml'
        dmp.save_dict()


if __name__ == '__main__':
    app = PyDictApp()
    app.main()