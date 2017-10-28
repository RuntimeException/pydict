from PyQt5.QtCore import QObject, QAbstractListModel, QModelIndex, Qt
from dictmdl import IDictModel

class WordListModel(QAbstractListModel):
    def __init__(self, dictmdl: IDictModel = {}, parent: QObject = None, **kwargs):
        super().__init__(parent, **kwargs)
        self._dictmdl = dictmdl

    @property
    def dictmdl(self) -> IDictModel:
        return self._dictmdl

    @dictmdl.setter
    def dictmdl(self, value: IDictModel) -> None:
        assert (value is None) or isinstance(value, IDictModel), 'The dictmdl property of {} class shall have {} type.'\
               .format(self.__class__.__name__, IDictModel.__name__)
        self._dictmdl = value

    def rowCount(self, parent = QModelIndex()):
        return len(self._dictmdl)

    def data(self, index: QModelIndex, role: int, parent: QModelIndex = QModelIndex()):
        if role == Qt.DisplayRole:
            return str(self._dictmdl.get_wordlist(True, True)[index.row()])