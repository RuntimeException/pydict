from PyQt5.QtWidgets import QStyle, QTabWidget, QListView, QSplitter, QLabel, QComboBox, QPushButton, QLineEdit, QCheckBox
from PyQt5.QtWidgets import QMenu, QAction
from PyQt5.QtWidgets import QWidget, QMainWindow, QAbstractItemView, QApplication
from PyQt5.QtWidgets import QVBoxLayout, QGridLayout, QHBoxLayout, QDialog
from PyQt5.Qt import Qt, QPixmap, QIcon, QFont
from PyQt5.QtCore import QObject, QSize, QRect, QAbstractListModel, QItemSelection, QModelIndex
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from dictmdl import WordListModel, DictModel
from language.noun import Noun
from language.word import Word, WordClass
from language.article import GrammaticalGender
from event import EventBus, EventSource, EventSaveAll, EventId
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

        self.editmode = False

        self.l_wordedit_title = QLabel('')
        self.f_wordedit_title = self.l_wordedit_title.font()
        self.f_wordedit_title.setBold(True)
        self.f_wordedit_title.setPointSize(self.f_wordedit_title.pointSize() * 2)
        self.l_wordedit_title.setFont(self.f_wordedit_title)

        self.l_guid_title = QLabel(self.WORD_GUID_TEXT)
        self.l_guid = QLabel('')

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


    @property
    def eventbus(self) -> EventBus:
        return self._eventbus

    @eventbus.setter
    def eventbus(self, value: EventBus) -> None:
        assert isinstance(value, EventBus), 'The eventbus property of {} class shall have {} type.'\
               .format(self.__class__.__name__, EventBus.__name__)
        self._eventbus = value


    def init_editmode(self) -> None:
        if self.option == WordWidgetOption.WORD_EDIT_MODE:
            self.set_editable(False)
        elif self.option == WordWidgetOption.WORD_NEW_MODE:
            self.set_editable(True)
        else:
            raise NotImplementedError('Invalid {} value: {}.'
                  .format(WordWidgetOption.__class__.__name__, self.option.name))

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
            self.l_wordedit_title.setText('')
            self.l_guid.setText('')
        elif self.option == WordWidgetOption.WORD_NEW_MODE:
            self.l_wordedit_title.setText('New ' + self.word.get_wordclass().name)
            if self.word.guid is None:
                self.l_guid.setText('__None__')
            else:
                self.l_guid.setText(hex(self.word.guid))
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
        self.parse_view()
        self.update_view()
        if self.word is not None:
            if self.option == WordWidgetOption.WORD_EDIT_MODE:
                self.event_word_updated.emit(self.word)
            elif self.option == WordWidgetOption.WORD_NEW_MODE:
                self.event_word_added.emit(self.word)
        self.event_accept.emit()

    def handle_b_cancel_clicked(self) -> None:
        self.set_editable(False)
        self.update_view()
        self.event_reject.emit()

    event_word_added   = pyqtSignal(Word)
    event_word_removed = pyqtSignal(int)
    event_word_updated = pyqtSignal(Word)
    event_accept = pyqtSignal()
    event_reject = pyqtSignal()


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

        self.cmb_gender = QComboBox()
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

        self.cmb_gender.addItem(ico_blue,   GrammaticalGender.MASCULINE.name)
        self.cmb_gender.addItem(ico_green,  GrammaticalGender.NEUTRAL.name)
        self.cmb_gender.addItem(ico_red,    GrammaticalGender.FEMININE.name)
        self.cmb_gender.addItem(ico_yellow, GrammaticalGender.PLURAL.name)

        self.lgr_word.addWidget(self.l_wordedit_title, 0, 0, 1, 3, Qt.AlignHCenter)
        self.lgr_word.addLayout(self.lhb_cmdbtns, 1, 0, 1, 3)
        self.lgr_word.addWidget(self.l_guid_title, 2, 0)
        self.lgr_word.addWidget(self.l_gender_title, 3, 0)
        self.lgr_word.addWidget(self.l_nounsn_title, 4, 0)
        self.lgr_word.addWidget(self.l_nounpl_title, 5, 0)
        self.lgr_word.addWidget(self.l_guid, 2, 1, 1, 2)
        self.lgr_word.addWidget(self.cmb_gender, 3, 1, 1, 2)
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
        self.init_editmode()
        
        self.cmb_gender.currentIndexChanged.connect(self.handle_cmb_gender_textchange)


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
        self.set_editable(False)
        self.update_view()

    def parse_view(self) -> None:
        if self.noun is not None:
            self.noun.gender = self.parse_gender()
            self.noun.nounsn = self.parse_nounsn()
            self.noun.nounpl = self.parse_nounpl()
            if (self.noun.gender == GrammaticalGender.PLURAL) or (self.noun.nounsn == ''):
                self.noun.singular_exist = False
                self.noun.nounsn = ''
            else:
                self.noun.singular_exist = True

            if self.noun.nounpl == '':
                self.noun.plural_exist = False
            else:
                self.noun.plural_exist = True
                
            super().parse_view()


    def update_view(self) -> None:
        if self.noun is None:
            self.le_nounsn.setText('')
            self.le_nounpl.setText('')
            self.cmb_gender.setCurrentIndex(0)
        else:
            self.le_nounsn.setText(self.noun.nounsn or '')
            self.le_nounpl.setText(self.noun.nounpl or '')
            if self.noun.gender is not None:
                gender_cbidx = self.cmb_gender.findText(self.noun.gender.name)
            else:
                gender_cbidx = 0
            self.cmb_gender.setCurrentIndex(gender_cbidx)
            
            if self.noun.gender == GrammaticalGender.PLURAL:
                self.le_nounsn.setEnabled(False)
            else:
                if self.editmode:
                    self.le_nounsn.setEnabled(True)
                else:
                    self.le_nounsn.setEnabled(False)
        super().update_view()

    def set_editable(self, enable: bool) -> None:
        super().set_editable(enable)
        self.cmb_gender.setEnabled(enable)
        self.le_nounsn.setEnabled(enable)
        self.le_nounpl.setEnabled(enable)

    def parse_gender(self) -> GrammaticalGender:
        text = self.cmb_gender.currentText()
        if GrammaticalGender.__members__.get(text) is None:
            return GrammaticalGender.MASCULINE
        else:
            return GrammaticalGender[text]

    def parse_nounsn(self) -> str:
        return self.le_nounsn.text().strip()

    def parse_nounpl(self) -> str:
        return self.le_nounpl.text().strip()

    def handle_cmb_gender_textchange(self, text: str) -> None:
        if self.parse_gender() == GrammaticalGender.PLURAL:
            self.le_nounsn.setEnabled(False)
        else:
            if self.editmode:
                self.le_nounsn.setEnabled(True)
            else:
                self.le_nounsn.setEnabled(False)


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
    def eventbus(self) -> EventBus:
        return self._eventbus

    @eventbus.setter
    def eventbus(self, value: EventBus) -> None:
        assert isinstance(value, EventBus), 'The eventbus property of {} class shall have {} type.'\
               .format(self.__class__.__name__, EventBus.__name__)
        self._eventbus = value


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

    def __init__(self, wordclass: WordClass, model: WordListModel, parent = None, **kwargs):
        super().__init__(parent, **kwargs)
        
        self.word = None
        self.w_wordview = None

        self.layout = QVBoxLayout()

        if wordclass == WordClass.NOUN:
            self.word       = Noun()
            self.w_wordview = NounView(self.word, WordWidgetOption.WORD_NEW_MODE)
        else:
            raise NotImplementedError('WordDialog with unknown WordClass: {}.'.format(wordclass.name))

        self.wordlsmdl = model

        guid = self.wordlsmdl.allocate_guid()
        self.word.guid = guid
        self.w_wordview.update_view()

        self.layout.addWidget(self.w_wordview)
        self.setLayout(self.layout)


    @property
    def eventbus(self) -> EventBus:
        return self._eventbus

    @eventbus.setter
    def eventbus(self, value: EventBus) -> None:
        assert isinstance(value, EventBus), 'The eventbus property of {} class shall have {} type.'\
               .format(self.__class__.__name__, EventBus.__name__)
        self._eventbus = value


    @property
    def wordlsmdl(self) -> WordListModel:
        return self._wordlsmdl

    @wordlsmdl.setter
    def wordlsmdl(self, value: WordListModel) -> None:
        assert isinstance(value, WordListModel), 'The wordlsmdl property of {} class shall have {} type.'\
               .format(self.__class__.__name__, WordListModel.__name__)
        self._wordlsmdl = value
        self.connect_wordview(self.w_wordview)

    def connect_wordview(self, wordview: WordView) -> None:
        wordview.event_word_added.connect(self.wordlsmdl.add_word_request)
        wordview.event_accept.connect(self.handle_accept)
        wordview.event_reject.connect(self.handle_reject)
        
    def handle_accept(self) -> None:
        self.done(0)

    def handle_reject(self) -> None:
        self.done(1)    


class DictView(QWidget):
    BTN_ADDWORD_TEXT = 'Add'
    BTN_RMWORD_TEXT  = 'Remove'
    

    def __init__(self, parent: QObject = None, model: WordListModel = None, **kwargs):
        super().__init__(parent, **kwargs)

        self.lhb_control = QHBoxLayout()
        self.layout = QVBoxLayout()

        self.b_addword = QPushButton(self.BTN_ADDWORD_TEXT)
        self.b_rmword  = QPushButton(self.BTN_RMWORD_TEXT)
        self.cmb_wordclass = QComboBox()
        
        for wc in WordClass:
            self.cmb_wordclass.addItem(wc.name)

        self.hsplitter = QSplitter(Qt.Horizontal)

        self.wordlistview = QListView()
        self.wordeditview = WordEditView()

        self.wordlsmdl = model

        self.wordlistview.activated.connect(self.wordeditview.handle_wordlistitem_activated)

        self.hsplitter.addWidget(self.wordlistview)
        self.hsplitter.addWidget(self.wordeditview)
        self.hsplitter.setSizes([PyDictAppView.DESKTOP_DEFAULT_WIDTH * 0.4, PyDictAppView.DESKTOP_DEFAULT_WIDTH * 0.6])

        self.lhb_control.addWidget(self.cmb_wordclass)
        self.lhb_control.addWidget(self.b_addword)
        self.lhb_control.addWidget(self.b_rmword)
        self.lhb_control.addStretch()

        self.layout.addLayout(self.lhb_control)
        self.layout.addWidget(self.hsplitter)
        self.setLayout(self.layout)

        self.b_addword.clicked.connect(self.handle_b_addword_clicked)
        self.b_rmword.clicked.connect(self.handle_b_rmword_clicked)
        
    @property
    def eventbus(self) -> EventBus:
        return self._eventbus

    @eventbus.setter
    def eventbus(self, value: EventBus) -> None:
        assert isinstance(value, EventBus), 'The eventbus property of {} class shall have {} type.'\
               .format(self.__class__.__name__, EventBus.__name__)
        self._eventbus = value
        self.wordeditview.eventbus = self.eventbus

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
        word_dialog = WordDialog(wc, self.wordlsmdl, self)
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
        wordclass_text = self.cmb_wordclass.currentText()
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

    @property
    def eventbus(self) -> EventBus:
        return self._eventbus

    @eventbus.setter
    def eventbus(self, value: EventBus) -> None:
        assert isinstance(value, EventBus), 'The eventbus property of {} class shall have {} type.'\
               .format(self.__class__.__name__, EventBus.__name__)
        self._eventbus = value
        self.tab_dictview.eventbus = self.eventbus


class PyDictAppView(QMainWindow):
    DESKTOP_DEFAULT_WIDTH = 1280
    DESKTOP_DEFAULT_HEIGHT = 720

    def __init__(self, qapp: QApplication = None, **kwargs):
        super().__init__(**kwargs)

        self._eventbus = None
        self.eventsrc_saveall = EventSource(EventId.SAVE_ALL)
        self.qapp = qapp        

        if qapp is None:
            desktop_rect = QRect(0, 0, self.DESKTOP_DEFAULT_WIDTH, self.DESKTOP_DEFAULT_WIDTH)
        else:
            desktop_rect = self.qapp.desktop().availableGeometry()

        aligned_rect = QStyle.alignedRect(Qt.LeftToRight, Qt.AlignCenter, self.size(), desktop_rect)

        self.setWindowTitle('Default Title')
        self.setGeometry(aligned_rect)

        self.central_widget = PyDictCentralWidget()

        self.mn_file = self.menuBar().addMenu('&File')
        self.act_save = QAction('&Save', None)
        self.mn_file.addAction(self.act_save)

        self.act_save.triggered.connect(self.handle_act_save_triggered)
        self.setCentralWidget(self.central_widget)


    def handle_act_save_triggered(self, checked: bool) -> None:
        self.eventsrc_saveall.fire()


    @property
    def eventbus(self) -> EventBus:
        return self._eventbus


    @eventbus.setter
    def eventbus(self, value: EventBus) -> None:
        assert isinstance(value, EventBus), 'The eventbus property of {} class shall have {} type.'\
               .format(self.__class__.__name__, EventBus.__name__)
        if self.eventbus is not None:
            self.eventbus.remove_eventsrc(self.eventsrc_saveall)
        self._eventbus = value
        self.central_widget.eventbus = self.eventbus
        self._eventbus.add_eventsrc(self.eventsrc_saveall)


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


    @property
    def eventbus(self) -> EventBus:
        return self._eventbus

    @eventbus.setter
    def eventbus(self, value: EventBus) -> None:
        assert isinstance(value, EventBus), 'The eventbus property of {} class shall have {} type.'\
               .format(self.__class__.__name__, EventBus.__name__)
        self._eventbus = value


    def build(self) -> PyDictAppView:
        appview = PyDictAppView(self.qapp)
        appview.eventbus = self.eventbus
        appview.setWindowTitle(self.title)
        appview.central_widget.tab_dictview.wordlsmdl = self.dictmdl.create_wordlistmodel()
        return appview