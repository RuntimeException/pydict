from PyQt5.QtWidgets import QStyle, QTabWidget, QListView, QSplitter, QLabel, QComboBox, QPushButton, QLineEdit
from PyQt5.QtWidgets import QWidget, QMainWindow, QAbstractItemView, QApplication
from PyQt5.QtWidgets import QVBoxLayout, QGridLayout, QHBoxLayout
from PyQt5.Qt import Qt, QPixmap, QIcon, QFont
from PyQt5.QtCore import QObject, QSize, QRect, QAbstractListModel, QItemSelection, QModelIndex, pyqtSlot
from dictmdl import WordListModel, DictModel
from language.noun import Noun
from language.word import Word, WordClass
from language.article import GrammaticalGender
import copy


class WordWidget(QWidget):

    WORD_GUID_TEXT = 'GUID:'
    BTN_EDIT_TEXT = 'Edit'
    BTN_SAVE_TEXT = 'Save'
    BTN_CANCEL_TEXT = 'Cancel'

    def __init__(self, word: Word, parent: QObject = None, **kwargs):
        super().__init__(parent, **kwargs)

        if word.guid is None:
            guid_text = '__None__'
        else:
            guid_text = hex(word.guid)

        self.l_wordedit_title = QLabel(str(word))
        self.f_wordedit_title = self.l_wordedit_title.font()
        self.f_wordedit_title.setBold(True)
        self.f_wordedit_title.setPointSize(self.f_wordedit_title.pointSize() * 2)
        self.l_wordedit_title.setFont(self.f_wordedit_title)

        self.l_guid_title = QLabel(self.WORD_GUID_TEXT)
        self.l_guid = QLabel(guid_text)

        self.b_edit = QPushButton(self.BTN_EDIT_TEXT)
        self.b_save = QPushButton(self.BTN_SAVE_TEXT)
        self.b_cancel = QPushButton(self.BTN_CANCEL_TEXT)

        self.hbl_cmdbtns = QHBoxLayout()
        self.hbl_cmdbtns.addWidget(self.b_edit)
        self.hbl_cmdbtns.addWidget(self.b_save)
        self.hbl_cmdbtns.addWidget(self.b_cancel)

        self.b_edit.clicked.connect(self.handle_b_edit_clicked)
        self.b_save.clicked.connect(self.handle_b_save_clicked)
        self.b_cancel.clicked.connect(self.handle_b_cancel_clicked)


    def set_editable(self, enable: bool) -> None:
        self.editmode = enable
        self.b_edit.setEnabled(not enable)
        self.b_save.setEnabled(enable)
        self.b_cancel.setEnabled(enable)

    @property
    def editmode(self) -> bool:
        return self._editmode

    @editmode.setter
    def editmode(self, value: bool) -> None:
        assert (value is None) or isinstance(value, bool), 'The editmode property of {} class shall have {} type.'\
               .format(self.__class__.__name__, bool.__name__)
        self._editmode = value


    def handle_b_edit_clicked(self):
        self.set_editable(True)

    def handle_b_save_clicked(self):
        self.set_editable(False)

    def handle_b_cancel_clicked(self):
        self.set_editable(False)



class NounView(WordWidget):
    NOUN_GENDER_LABEL_TEXT = 'Gender:'
    NOUNSN_LABEL_TEXT = 'Singular:'
    NOUNPL_LABEL_TEXT = 'Plural:'
    ICON_DEFAULT_SIZE = 16
    
    def __init__(self, noun: Noun, parent: QObject = None, **kwargs):
        super().__init__(noun, parent, **kwargs)

        self.noun = copy.deepcopy(noun)
        
        self.l_gender_title = QLabel(self.NOUN_GENDER_LABEL_TEXT) 
        self.l_nounsn_title = QLabel(self.NOUNSN_LABEL_TEXT) 
        self.l_nounpl_title = QLabel(self.NOUNPL_LABEL_TEXT) 

        self.cb_gender = QComboBox() 
        self.le_nounsn = QLineEdit(self.noun.nounsn) 
        self.le_nounpl = QLineEdit(self.noun.nounpl)

        self.grl_word = QGridLayout()

        px_red    = QPixmap(self.ICON_DEFAULT_SIZE, self.ICON_DEFAULT_SIZE)
        px_green  = QPixmap(self.ICON_DEFAULT_SIZE, self.ICON_DEFAULT_SIZE)
        px_blue   = QPixmap(self.ICON_DEFAULT_SIZE, self.ICON_DEFAULT_SIZE)
        px_yellow = QPixmap(self.ICON_DEFAULT_SIZE, self.ICON_DEFAULT_SIZE)

        px_red.fill(Qt.red)
        px_green.fill(Qt.green)
        px_blue.fill(Qt.blue)
        px_yellow.fill(Qt.yellow)

        px_red    = QIcon(px_red)
        px_green  = QIcon(px_green)
        px_blue   = QIcon(px_blue)
        px_yellow = QIcon(px_yellow)

        #self.cb_gender.setIconSize(QSize(16, 16))
        self.cb_gender.addItem(px_blue, GrammaticalGender.MASCULINE.name)
        self.cb_gender.addItem(px_green, GrammaticalGender.NEUTRAL.name)
        self.cb_gender.addItem(px_red, GrammaticalGender.FEMININE.name)
        self.cb_gender.addItem(px_yellow, GrammaticalGender.PLURAL.name)

        self.grl_word.addWidget(self.l_wordedit_title, 0, 0, 1, 3, Qt.AlignHCenter)
        self.grl_word.addLayout(self.hbl_cmdbtns, 1, 0, 1, 3)
        self.grl_word.addWidget(self.l_guid_title, 2, 0)
        self.grl_word.addWidget(self.l_gender_title, 3, 0)
        self.grl_word.addWidget(self.l_nounsn_title, 4, 0)
        self.grl_word.addWidget(self.l_nounpl_title, 5, 0)
        self.grl_word.addWidget(self.l_guid, 2, 1, 1, 2)
        self.grl_word.addWidget(self.cb_gender, 3, 1, 1, 2)
        self.grl_word.addWidget(self.le_nounsn, 4, 1, 1, 2)
        self.grl_word.addWidget(self.le_nounpl, 5, 1, 1, 2)

        self.grl_word.setColumnStretch(0, 10)
        self.grl_word.setColumnStretch(1, 12)
        self.grl_word.setColumnStretch(2, 12)
        self.grl_word.setColumnStretch(3, 66)
        self.grl_word.setRowStretch(0, 10)
        self.grl_word.setRowStretch(6, 90)

        self.setLayout(self.grl_word)
        self.set_editable(False)


    @property
    def noun(self) -> Noun:
        return self._noun

    @noun.setter
    def noun(self, value: Noun) -> None:
        assert (value is None) or isinstance(value, Noun), 'The noun property of {} class shall have {} type.'\
               .format(self.__class__.__name__, Noun.__name__)
        self._noun = value

    def set_editable(self, enable: bool) -> None:
        super().set_editable(enable)
        self.cb_gender.setEnabled(enable)
        self.le_nounsn.setEnabled(enable)
        self.le_nounpl.setEnabled(enable)


class WordEditView(QWidget):

    def __init__(self, parent: QObject = None, model: WordListModel = None, **kwargs):
        super().__init__(parent, **kwargs)
        self.wordlsmdl = model
        
        self.layout = QVBoxLayout()
        self.wordview = QLabel('Empty')

        self.layout.addWidget(self.wordview)

        self.setLayout(self.layout)


    @property
    def wordlsmdl(self) -> WordListModel:
        return self._wordlsmdl

    @wordlsmdl.setter
    def wordlsmdl(self, value: WordListModel) -> None:
        assert (value is None) or isinstance(value, WordListModel), 'The wordlsmdl property of {} class shall have {} type.'\
               .format(self.__class__.__name__, WordListModel.__name__)
        self._wordlsmdl = value


    @pyqtSlot(QModelIndex)
    def on_wordlistitem_activated(self, mdlidx: QModelIndex) -> None:
        wordview = None
        if self.wordlsmdl is not None:
            word = self.wordlsmdl.get_word(mdlidx)
            if word.get_wordclass() == WordClass.NOUN:
                wordview = self.create_nounview(word)
            else:
                # TODO: add further wordclasses
                pass
        if wordview is not None:
            self.layout.removeWidget(self.wordview)
            self.wordview.deleteLater()
            self.wordview = wordview
            self.layout.insertWidget(1, self.wordview)

    def create_nounview(self, noun: Noun) -> NounView:
        nounview = NounView(noun)
        return nounview



class DictView(QWidget):
    def __init__(self, parent: QObject = None, model: WordListModel = None, **kwargs):
        super().__init__(parent, **kwargs)

        self.layout = QVBoxLayout()
        self.hsplitter = QSplitter(Qt.Horizontal)

        self.wordlistview = QListView()
        self.wordeditview = WordEditView()        

        self.wordlsmdl = model

        self.wordlistview.activated.connect(self.wordeditview.on_wordlistitem_activated)

        self.hsplitter.addWidget(self.wordlistview)
        self.hsplitter.addWidget(self.wordeditview)
        self.hsplitter.setSizes([PyDictAppView.DESKTOP_DEFAULT_WIDTH * 0.4, PyDictAppView.DESKTOP_DEFAULT_WIDTH * 0.6])
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
        self.wordeditview.wordlsmdl = value


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
    def __init__(self, dictmdl: DictModel = None, **kwargs):
        super().__init__(**kwargs)
        self._title = 'Default Title'
        if dictmdl is None:
            self.dictmdl = DictModel()
        else:
            self.dictmdl = dictmdl
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
    def dictmdl(self) -> DictModel:
        return self._dictmdl

    @dictmdl.setter
    def dictmdl(self, value: DictModel) -> None:
        if not isinstance(value, DictModel):
            raise TypeError('The dictmdl property of {} class shall have {} type.'
                            .format(self.__class__.__name__, DictModel.__name__))
        self._dictmdl = value


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
        appview.central_widget.tab_dictview.wordlsmdl = self.dictmdl.create_wordlistmodel()
        return appview