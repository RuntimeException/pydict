import abc
import numbers
from abc import ABC
from language.word import Word
from PyQt5.QtCore import QObject, QAbstractListModel, QAbstractTableModel, QModelIndex
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5.Qt import Qt, QPixmap, QIcon, QFont, QColor

   
class DictModel(QObject):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._worddict = {}
        self._maxguid = -1
        self._guid_alloc_en = False

    def allocate_guid(self) -> int:
        if self.guid_alloc_en:
            self._maxguid += 1
            return self._maxguid
        else:
            raise Exception('GUID allocation attempt when it is explicitly forbidden.')

    @property
    def guid_alloc_en(self) -> bool:
        return self._guid_alloc_en

    @guid_alloc_en.setter
    def guid_alloc_en(self, value: bool) -> None:
        if not isinstance(value, bool):
            raise TypeError('The guid_alloc_en property of {} class shall have {} type.'
                            .format(self.__class__.__name__, bool.__name__))
        self._guid_alloc_en = value

    def add_word(self, word: Word) -> None:
        assert isinstance(word, Word), 'The word parameter of {} method in {} class shall have {} type.'\
               .format(self.add_word.__name__, self.__class__.__name__, Word.__name__)
        assert (word.guid not in self._worddict), 'The guid property of the word parameter of {} method in {} class shall '\
               'not exist in dictionary model. (guid: {})'.format(self.add_word.__name__,self.__class__.__name__,word.guid)
        self._worddict[word.guid] = word
        if word.guid > self._maxguid:
            self._maxguid = word.guid
        self.event_word_added.emit(word)


    def remove_word(self, guid: int) -> Word:
        assert isinstance(guid, int), 'The guid parameter of {} method in {} class shall have {} type.'\
               .format(self.remove_word.__name__, self.__class__.__name__, int.__name__)
        self.event_word_removed.emit(self._worddict[guid])
        word = self._worddict.pop(guid)
        return word


    def update_word(self, word) -> None:
        assert isinstance(word, Word), 'The word parameter of {} method in {} class shall have {} type.'\
               .format(self.update_word.__name__, self.__class__.__name__, Word.__name__)
        assert (word.guid in self._worddict), 'The guid property of the word parameter of {} method in {} class shall '\
               'exist in dictionary model. (guid: {})'.format(self.update_word.__name__,self.__class__.__name__,word.guid)
        self._worddict[word.guid] = word
        self.event_word_updated.emit(word)


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

    def get_wordguidlist(self) -> list:
        return list(self._worddict.keys())

    def __len__(self) -> int:
        return len(self._worddict)


    def create_wordlistmodel(self) -> QAbstractListModel:
        wlsmdl = WordListModel(self)
        return wlsmdl

    event_word_added = pyqtSignal(Word)

    event_word_removed = pyqtSignal(Word)

    event_word_updated = pyqtSignal(Word)
        
        

class WordListModel(QAbstractListModel):
    ICON_DEFAULT_SIZE = 16
    ICON_DEFAULT_BRIGHTNESS = 0.8

    def __init__(self, dictmdl: DictModel, parent: QObject = None, **kwargs):
        super().__init__(parent, **kwargs)
        self.dictmdl = dictmdl        

    def allocate_guid(self) -> int:
        return self.dictmdl.allocate_guid()

    @property
    def dictmdl(self) -> DictModel:
        return self._dictmdl

    @dictmdl.setter
    def dictmdl(self, value: DictModel) -> None:
        assert isinstance(value, DictModel), 'The dictmdl property of {} class shall have {} type.'\
               .format(self.__class__.__name__, DictModel.__name__)
        if hasattr(self, '_dictmdl'):
            self.dictmdl.event_word_added.disconnect(self.handle_word_added)
            self.dictmdl.event_word_removed.disconnect(self.handle_word_removed)
            self.dictmdl.event_word_updated.disconnect(self.handle_word_modified)
        
        self._dictmdl = value
        self._guidlist = self.dictmdl.get_wordguidlist()

        self.dictmdl.event_word_added.connect(self.handle_word_added)
        self.dictmdl.event_word_removed.connect(self.handle_word_removed)
        self.dictmdl.event_word_updated.connect(self.handle_word_updated)


    def rowCount(self, parent = QModelIndex()):
        return len(self._guidlist)

    def data(self, index: QModelIndex, role: int, parent: QModelIndex = QModelIndex()):
        if role == Qt.DisplayRole:
            return str(self.get_word(index))

        if role == Qt.DecorationRole:
            pixmap = QPixmap(self.ICON_DEFAULT_SIZE, self.ICON_DEFAULT_SIZE)
            quality = self.get_word(index).get_quality()
            green = max(min((quality * 255 * self.ICON_DEFAULT_BRIGHTNESS), 255), 0)
            red =  max(min(((1.0 - quality) * 255 * self.ICON_DEFAULT_BRIGHTNESS), 255), 0)
            color = QColor(red, green, 0)
            pixmap.fill(color)
            icon = QIcon(pixmap)
            return icon
            

    def get_guid(self, index: QModelIndex) -> int:
        return self._guidlist[index.row()]

    def get_word(self, index: QModelIndex) -> Word:
        guid = self.get_guid(index)
        return self.dictmdl.get_word(guid)

    def insertRows(self, row: int, count: int, parent: QModelIndex) -> None:
        raise NotImplementedError('The insertRows is not implemented in WordListModel.')
        
    def removeRows(self, row: int, count: int, parent: QModelIndex) -> None:
        guidrmls = self._guidlist[row : row + count]
        for guid in guidrmls:
            self.dictmdl.remove_word(guid)
        
    def add_word_request(self, word: Word) -> bool:
        self.dictmdl.add_word(word)
        return True

    def remove_word_request(self, guid: int) -> bool:
        self.dictmdl.remove_word(guid)
        return True

    def update_word_request(self, word: Word) -> bool:
        self.dictmdl.update_word(word)
        return True
    

    @pyqtSlot(Word)
    def handle_word_added(self, word: Word) -> None:
        print('Added - ' + str(word))
        self.beginInsertRows(QModelIndex(), len(self._guidlist), len(self._guidlist))
        self._guidlist.append(word.guid)
        self.endInsertRows()


    @pyqtSlot(Word)
    def handle_word_removed(self, word: Word) -> None:
        print('Removed - ' + str(word))
        self.beginRemoveRows(QModelIndex(), self._guidlist.index(word.guid), self._guidlist.index(word.guid))
        self._guidlist.remove(word.guid)
        self.endRemoveRows()


    @pyqtSlot(Word)
    def handle_word_updated(self, word: Word) -> None:
        row = self._guidlist.index(word.guid)
        self.dataChanged.emit(self.index(row), self.index(row))
        print('Modified - ' + str(word))