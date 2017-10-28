from PyQt5.QtWidgets import QWidget, QMainWindow, QStyle, QTabWidget, QVBoxLayout, QApplication, QListView, QSplitter, QLabel
from PyQt5.Qt import Qt
from PyQt5.QtCore import QObject, QSize, QRect, QAbstractListModel
from adapter import WordListModel


class NounView(QWidget):
    NOUN_GENDER_LABEL_TEXT = 'Gender'
    NOUNSN_LABEL_TEXT = 'Singular'
    NOUNPL_LABEL_TEXT = 'Plural'
    
    def __init__(self, parent: QObject = None, **kwargs):
        super().__init__(parent, **kwargs)
        
        self.layout = QVBoxLayout()
        
        self.label = QLabel('Teszt') 

        self.layout.addWidget(self.label)
        self.setLayout(self.layout)
    

    pass


class DictView(QWidget):
    def __init__(self, parent: QObject = None, model: WordListModel = None, **kwargs):
        super().__init__(parent, **kwargs)


        self.layout = QVBoxLayout()
        self.hsplitter = QSplitter(Qt.Horizontal)

        self.wordlistview = QListView()
        self.wordlistview.setModel(model)

        self.wordview = NounView()

        self.hsplitter.addWidget(self.wordlistview)
        self.hsplitter.addWidget(self.wordview)
        self.layout.addWidget(self.hsplitter)
        self.setLayout(self.layout)

    @property
    def wordlsmdl(self) -> WordListModel:
        return self.wordlistview.model()

    @wordlsmdl.setter
    def wordlsmdl(self, value: WordListModel) -> None:
        assert (value is None) or isinstance(value, WordListModel), 'The wordlsmdl property of {} class shall have {} type.'\
               .format(self.__class__.__name__, WordListModel.__name__)
        self.wordlistview.setModel(value)


class PyDictCentralWidget(QWidget):
    def __init__(self, parent: QObject = None, **kwargs):
        super().__init__(parent, **kwargs)        

        self.layout = QVBoxLayout(self)
        
        self.tabs = QTabWidget()
        self.tab_dictview = DictView()
        self.tab_exerciseview = QWidget()

        self.tabs.addTab(self.tab_dictview, 'Dictionary')
        self.tabs.addTab(self.tab_exerciseview, 'Exercise')
    
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)


class PyDictAppView(QMainWindow):
    DESKTOP_DEFAULT_WIDTH = 1280
    DESKTOP_DEFAULT_HEIGHT = 720

    def __init__(self, qapp: QApplication = None, **kwargs):
        super().__init__(**kwargs)
        self.qapp = qapp        

        if qapp is None:
            desktop_rect = QRect(0, 0, self.DESKTOP_DEFAULT_WIDTH, self.DESKTOP_DEFAULT_WIDTH)
        else:
            desktop_rect = self.qapp.desktop().availableGeometry()

        aligned_rect = QStyle.alignedRect(Qt.LeftToRight, Qt.AlignCenter, self.size(), desktop_rect)

        self.setWindowTitle('Default Title')
        self.setGeometry(aligned_rect)

        self.central_widget = PyDictCentralWidget()
        self.setCentralWidget(self.central_widget)


class PyDictGuiBuilder(object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._title = 'Default Title'
        self._wordlsmdl = WordListModel()
        self._qapp = None

    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, value: str) -> None:
        assert (value is None) or isinstance(value, str), 'The title property of {} class shall have {} type.'\
               .format(self.__class__.__name__, str.__name__)
        self._title = value


    @property
    def wordlsmdl(self) -> WordListModel:
        return self._wordlsmdl

    @wordlsmdl.setter
    def wordlsmdl(self, value: WordListModel) -> None:
        assert (value is None) or isinstance(value, WordListModel), 'The wordlsmdl property of {} class shall have {} type.'\
               .format(self.__class__.__name__, WordListModel.__name__)
        self._wordlsmdl = value


    @property
    def qapp(self) -> QApplication:
        return self._qapp

    @qapp.setter
    def qapp(self, value: QApplication) -> None:
        assert (value is None) or isinstance(value, QApplication), 'The qapp property of {} class shall have {} type.'\
               .format(self.__class__.__name__, QApplication.__name__)
        self._qapp = value

    def build(self) -> PyDictAppView:
        appview = PyDictAppView(self.qapp)
        appview.setWindowTitle(self.title)
        appview.central_widget.tab_dictview.wordlsmdl = self.wordlsmdl
        return appview