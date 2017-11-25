from PyQt5.QtWidgets import QStyle, QTabWidget, QListView, QSplitter, QLabel, QComboBox, QPushButton, QLineEdit
from PyQt5.QtWidgets import QWidget, QMainWindow, QAbstractItemView, QApplication
from PyQt5.QtWidgets import QVBoxLayout, QGridLayout, QHBoxLayout, QDialog
from PyQt5.Qt import Qt, QPixmap, QIcon, QFont
from PyQt5.QtCore import QObject, QSize, QRect, QAbstractListModel, QItemSelection, QModelIndex
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from dictmdl import WordListModel, DictModel
from language.noun import Noun
from language.word import Word, WordClass
from language.article import GrammaticalGender
from enum import Enum
import copy

class WordWidgetOption(Enum):
    WORD_EDIT_MODE = 0
    WORD_NEW_MODE  = 1

class WordView(QWidget):

    WORD_GUID_TEXT = 'GUID:'
    BTN_EDIT_TEXT = 'Edit'
    BTN_SAVE_TEXT = 'Save'
    BTN_CANCEL_TEXT = 'Cancel'


    def __init__(self, word: Word, option: WordWidgetOption = None, parent: QObject = None, **kwargs):
        super().__init__(parent, **kwargs)

        if option is None:
            self.option = WordWidgetOption.WORD_EDIT_MODE
        else:
            self.option = option

        if (word is None) or (word.guid is None):
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

        if self.option == WordWidgetOption.WORD_EDIT_MODE:
            self.b_edit = QPushButton(self.BTN_EDIT_TEXT)
        else:
            self.b_edit = None

        self.b_save = QPushButton(self.BTN_SAVE_TEXT)
        self.b_cancel = QPushButton(self.BTN_CANCEL_TEXT)

        self.lhb_cmdbtns = QHBoxLayout()
        if self.option == WordWidgetOption.WORD_EDIT_MODE:
            self.lhb_cmdbtns.addWidget(self.b_edit)
        self.lhb_cmdbtns.addWidget(self.b_save)
        self.lhb_cmdbtns.addWidget(self.b_cancel)

        
        if self.option == WordWidgetOption.WORD_EDIT_MODE:
            self.b_edit.clicked.connect(self.handle_b_edit_clicked)
        self.b_save.clicked.connect(self.handle_b_save_clicked)
        self.b_cancel.clicked.connect(self.handle_b_cancel_clicked)


    def set_editable(self, enable: bool) -> None:
        self.editmode = enable
        if (self.option is not None) and (self.option == WordWidgetOption.WORD_EDIT_MODE):
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
    
    @property
    def word(self) -> Word:
        raise NotImplementedError('The word property of {} shall be overridden.', self.__class__.__name__)

    def update_view(self) -> None:
        if self.word is None:
            self.l_wordedit_title.setText('__None__')
            self.l_guid.setText('__None__')
        else:
            self.l_wordedit_title.setText(str(self.word))
            if self.word.guid is None:
                self.l_guid.setText('__None__')
            else:
                self.l_guid.setText(hex(self.word.guid))

    def parse_view(self) -> None:
        if self.word is not None:
            self.l_wordedit_title.setText(str(self.word))

    def handle_b_edit_clicked(self) -> None:
        self.set_editable(True)

    def handle_b_save_clicked(self) -> None:
        self.set_editable(False)
        self.update_view()
        if self.word is not None:
            if self.option == WordWidgetOption.WORD_EDIT_MODE:
                self.event_word_updated.emit(self.word)
            elif self.option == WordWidgetOption.WORD_NEW_MODE:
                self.event_word_added.emit(self.word)

    def handle_b_cancel_clicked(self) -> None:
        self.set_editable(False)
        self.update_view()

    event_word_added   = pyqtSignal(Word)
    event_word_removed = pyqtSignal(int)
    event_word_updated = pyqtSignal(Word)


class NounView(WordView):
    NOUN_GENDER_LABEL_TEXT = 'Gender:'
    NOUNSN_LABEL_TEXT = 'Singular:'
    NOUNPL_LABEL_TEXT = 'Plural:'
    ICON_DEFAULT_SIZE = 16
    
    def __init__(self, noun: Noun, option: WordWidgetOption = None, parent: QObject = None, **kwargs):
        super().__init__(noun, option, parent, **kwargs)
      
        self.l_gender_title = QLabel(self.NOUN_GENDER_LABEL_TEXT) 
        self.l_nounsn_title = QLabel(self.NOUNSN_LABEL_TEXT) 
        self.l_nounpl_title = QLabel(self.NOUNPL_LABEL_TEXT) 

        self.cb_gender = QComboBox() 
        self.le_nounsn = QLineEdit() 
        self.le_nounpl = QLineEdit()

        self.lgr_word = QGridLayout()

        px_red    = QPixmap(self.ICON_DEFAULT_SIZE, self.ICON_DEFAULT_SIZE)
        px_green  = QPixmap(self.ICON_DEFAULT_SIZE, self.ICON_DEFAULT_SIZE)
        px_blue   = QPixmap(self.ICON_DEFAULT_SIZE, self.ICON_DEFAULT_SIZE)
        px_yellow = QPixmap(self.ICON_DEFAULT_SIZE, self.ICON_DEFAULT_SIZE)

        px_red.fill(Qt.red)
        px_green.fill(Qt.green)
        px_blue.fill(Qt.blue)
        px_yellow.fill(Qt.yellow)

        ico_red    = QIcon(px_red)
        ico_green  = QIcon(px_green)
        ico_blue   = QIcon(px_blue)
        ico_yellow = QIcon(px_yellow)

        ico_red.addPixmap(px_red, QIcon.Disabled)
        ico_green.addPixmap(px_green, QIcon.Disabled)
        ico_blue.addPixmap(px_blue, QIcon.Disabled)
        ico_yellow.addPixmap(px_yellow, QIcon.Disabled)

        self.cb_gender.addItem(ico_blue,   GrammaticalGender.MASCULINE.name)
        self.cb_gender.addItem(ico_green,  GrammaticalGender.NEUTRAL.name)
        self.cb_gender.addItem(ico_red,    GrammaticalGender.FEMININE.name)
        self.cb_gender.addItem(ico_yellow, GrammaticalGender.PLURAL.name)

        self.lgr_word.addWidget(self.l_wordedit_title, 0, 0, 1, 3, Qt.AlignHCenter)
        self.lgr_word.addLayout(self.lhb_cmdbtns, 1, 0, 1, 3)
        self.lgr_word.addWidget(self.l_guid_title, 2, 0)
        self.lgr_word.addWidget(self.l_gender_title, 3, 0)
        self.lgr_word.addWidget(self.l_nounsn_title, 4, 0)
        self.lgr_word.addWidget(self.l_nounpl_title, 5, 0)
        self.lgr_word.addWidget(self.l_guid, 2, 1, 1, 2)
        self.lgr_word.addWidget(self.cb_gender, 3, 1, 1, 2)
        self.lgr_word.addWidget(self.le_nounsn, 4, 1, 1, 2)
        self.lgr_word.addWidget(self.le_nounpl, 5, 1, 1, 2)

        self.lgr_word.setColumnStretch(0, 10)
        self.lgr_word.setColumnStretch(1, 12)
        self.lgr_word.setColumnStretch(2, 12)
        self.lgr_word.setColumnStretch(3, 66)
        self.lgr_word.setRowStretch(0, 10)
        self.lgr_word.setRowStretch(6, 90)

        self.setLayout(self.lgr_word)

        self.noun = noun
        self.set_editable(False)

    @property
    def word(self) -> Word:
        return self.noun

    @property
    def noun(self) -> Noun:
        return self._noun

    @noun.setter
    def noun(self, noun: Noun) -> None:
        assert (noun is None) or isinstance(noun, Noun), 'The noun property of {} class shall have {} type.'\
               .format(self.__class__.__name__, Noun.__name__)
        self._noun = noun
        self.update_view()


    def parse_view(self) -> None:
        if self.noun is not None:
            self.noun.gender = self.parse_gender()
            self.noun.nounsn = self.parse_nounsn()
            self.noun.nounpl = self.parse_nounpl()
            super().parse_view()

    def update_view(self) -> None:
        if self.noun is None:
            self.le_nounsn.setText('')
            self.le_nounpl.setText('')
            self.cb_gender.setCurrentIndex(0)
        else:
            self.le_nounsn.setText(self.noun.nounsn or '')
            self.le_nounpl.setText(self.noun.nounpl or '')
            if self.noun.gender is not None:
                gender_cbidx = self.cb_gender.findText(self.noun.gender.name)
            else:
                gender_cbidx = 0
            self.cb_gender.setCurrentIndex(gender_cbidx)
        super().update_view()

    def set_editable(self, enable: bool) -> None:
        super().set_editable(enable)
        self.cb_gender.setEnabled(enable)
        self.le_nounsn.setEnabled(enable)
        self.le_nounpl.setEnabled(enable)

    def parse_gender(self) -> GrammaticalGender:
        text = self.cb_gender.currentText()
        if GrammaticalGender.__members__.get(text) is None:
            return GrammaticalGender.MASCULINE
        else:
            return GrammaticalGender[text]

    def parse_nounsn(self) -> str:
        return self.le_nounsn.text()

    def parse_nounpl(self) -> str:
        return self.le_nounpl.text()

    def handle_b_save_clicked(self):
        self.parse_view()
        self.update_view()
        super().handle_b_save_clicked()


class WordEditView(QWidget):

    def __init__(self, parent: QObject = None, model: WordListModel = None, **kwargs):
        super().__init__(parent, **kwargs)
        self.wordlsmdl = model
        
        self.layout = QVBoxLayout()

        self.l_empty = QLabel('Please select a word from the list.')
        self.w_nounview = NounView(None)
        
        self.w_nounview.hide()

        self.layout.addWidget(self.l_empty)
        self.layout.addWidget(self.w_nounview)

        self.setLayout(self.layout)


    @property
    def wordlsmdl(self) -> WordListModel:
        return self._wordlsmdl

    @wordlsmdl.setter
    def wordlsmdl(self, value: WordListModel) -> None:
        assert (value is None) or isinstance(value, WordListModel), 'The wordlsmdl property of {} class shall have {} type.'\
               .format(self.__class__.__name__, WordListModel.__name__)
        if hasattr(self, '_wordlsmdl') and (self._wordlsmdl is not None):
            self.disconnect_wordview(self._wordlsmdl)
        self._wordlsmdl = value
        if value is not None:
            self.connect_wordview(self.w_nounview)

    @pyqtSlot(QModelIndex)
    def handle_wordlistitem_activated(self, mdlidx: QModelIndex) -> None:
        wordview = None
        if self.wordlsmdl is not None:
            word = self.wordlsmdl.get_word(mdlidx)
            self.activate_wordview(word)

    def connect_wordview(self, wordview: WordView) -> None:
        wordview.event_word_added.connect(self.wordlsmdl.add_word_request)
        wordview.event_word_removed.connect(self.wordlsmdl.remove_word_request)
        wordview.event_word_updated.connect(self.wordlsmdl.update_word_request)

    def disconnect_wordview(self, wordview: WordView) -> None:
        wordview.event_word_added.disconnect(self.wordlsmdl.add_word_request)
        wordview.event_word_removed.disconnect(self.wordlsmdl.remove_word_request)
        wordview.event_word_updated.disconnect(self.wordlsmdl.update_word_request)

    def activate_wordview(self, word: Word) -> None:
        if word is None:
            self.l_empty.show()
            self.w_nounview.hide()
        elif word.get_wordclass() == WordClass.NOUN:
            self.l_empty.hide()
            self.w_nounview.noun = word
            self.w_nounview.show()
        else:
            raise NotImplementedError('Invalid WordClass in activate_wordview of {} class.'.format(self.__class__.__name__))


class WordDialog(QDialog):

    def __init__(self, wordclass: WordClass, parent = None, **kwargs):
        super().__init__(parent, **kwargs)
        
        self.word = None
        self.wordview = None

        self.layout = QVBoxLayout()

        if wordclass == WordClass.NOUN:
            self.word = Noun()
            self.wordview = NounView(self.word, WordWidgetOption.WORD_NEW_MODE)
        else:
            pass

        self.layout.addWidget(self.wordview)
        self.setLayout(self.layout)


class DictView(QWidget):
    BTN_ADDWORD_TEXT = 'Add'
    BTN_RMWORD_TEXT  = 'Remove'
    

    def __init__(self, parent: QObject = None, model: WordListModel = None, **kwargs):
        super().__init__(parent, **kwargs)

        self.lhb_control = QHBoxLayout()
        self.layout = QVBoxLayout()

        self.b_addword = QPushButton(self.BTN_ADDWORD_TEXT)
        self.b_rmword  = QPushButton(self.BTN_RMWORD_TEXT)
        self.cb_wordclass = QComboBox()
        
        for wc in WordClass:
            self.cb_wordclass.addItem(wc.name)

        self.hsplitter = QSplitter(Qt.Horizontal)

        self.wordlistview = QListView()
        self.wordeditview = WordEditView()

        self.wordlsmdl = model

        self.wordlistview.activated.connect(self.wordeditview.handle_wordlistitem_activated)

        self.hsplitter.addWidget(self.wordlistview)
        self.hsplitter.addWidget(self.wordeditview)
        self.hsplitter.setSizes([PyDictAppView.DESKTOP_DEFAULT_WIDTH * 0.4, PyDictAppView.DESKTOP_DEFAULT_WIDTH * 0.6])

        self.lhb_control.addWidget(self.cb_wordclass)
        self.lhb_control.addWidget(self.b_addword)
        self.lhb_control.addWidget(self.b_rmword)
        self.lhb_control.addStretch()

        self.layout.addLayout(self.lhb_control)
        self.layout.addWidget(self.hsplitter)
        self.setLayout(self.layout)

        self.b_addword.clicked.connect(self.handle_b_addword_clicked)
        self.b_rmword.clicked.connect(self.handle_b_rmword_clicked)
        

    @property
    def wordlsmdl(self) -> WordListModel:
        return self.wordlistview.model()

    @wordlsmdl.setter
    def wordlsmdl(self, value: WordListModel) -> None:
        assert (value is None) or isinstance(value, WordListModel), 'The wordlsmdl property of {} class shall have {} type.'\
               .format(self.__class__.__name__, WordListModel.__name__)
        self.wordlistview.setModel(value)
        self.wordeditview.wordlsmdl = value

    def handle_b_addword_clicked(self) -> None:
        wc = self.parse_wordclass()
        word_dialog = WordDialog(wc, self)
        word_dialog.show()
        word_dialog.exec()

    def handle_b_rmword_clicked(self) -> None:
        self.wordeditview.activate_wordview(None)
        sel_indexes = self.wordlistview.selectionModel().selectedIndexes()
        if sel_indexes is not None:
            for index in sel_indexes:
                guid = self.wordlsmdl.get_guid(index)
                self.wordlsmdl.remove_word_request(guid)

    def parse_wordclass(self) -> WordClass:
        wordclass_text = self.cb_wordclass.currentText()
        if WordClass.__members__.get(wordclass_text) is None:
            return WordClass.NOUN
        else:
            return WordClass[wordclass_text]


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