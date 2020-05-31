import sys
import abc
import json
import numbers
import logging
import logging.config
from abc import ABC
from persistence import XmlDictMdlPersistence
from view import PyDictAppView
from dictmdl import WordListModel
from PyQt5.QtWidgets import QApplication
from event import EventId, Event, EventSaveAll


logging.basicConfig()
with open('logging.json', 'r') as fd:
    logging.config.dictConfig(json.load(fd))
logger = logging.getLogger('pydict')


class PyDictApp(object):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._qapp = None
        self._dictmdl = None
        self._appview = None
        self._eventlogger = logging.getLogger('event')
        EventSaveAll.subscribe(self.handler_saveall)

    def main(self) -> None:
        dmp = XmlDictMdlPersistence()
        dmp.path = 'dict.xml'
        dmp.load_dict()
        print(dmp.to_string())

        self._dictmdl = dmp.dictmdl
        self._qapp = QApplication(sys.argv)

        self._appview = PyDictAppView(self._qapp)
        self._appview.setWindowTitle('PyDict')
        self._appview.central_widget.tab_dictview.wordlsmdl = self._dictmdl.create_wordlistmodel()
        self._appview.show()

        sys.exit(self._qapp.exec_())


    def handler_saveall(self, event: EventSaveAll, *args, **kwargs) -> None:
        dmp = XmlDictMdlPersistence()
        dmp.dictmdl = self._dictmdl
        dmp.path = 'dict.xml'
        dmp.save_dict()


if __name__ == '__main__':
    app = PyDictApp()
    app.main()