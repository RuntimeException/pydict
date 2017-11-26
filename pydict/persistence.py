import abc
import logging
from abc import ABC
from language.noun import Noun
from language.word import Word, WordClass
from language.article import GrammaticalGender, GrammaticalCase, ArticleType, Article
from lxml import etree
from dictmdl import DictModel

logger = logging.getLogger(__name__)


class DictMdlLoadException(Exception):
    ID_XML_INVALID_TAG = 'XmlInvalidTag'
    ID_XML_MISSING_TAG = 'XmlMissingTag'
    ID_XML_INVALID_TEXT = 'XmlInvalidText'
    ID_GUID_NOT_UNIQUE = 'GuidNotUnique'
    ID_XML_SYNTAX_ERR = 'XmlSyntaxError'

    def __init__(self, id: str, *args, **kwargs):
        super().__init__()
        self.xtext = 'NotFilledIn'
        if id == self.ID_XML_INVALID_TAG:
            self.xtext = id + '{{filepath: {filepath}, xmlpath: {xmlpath}, current_tag: '\
                              '{current_tag}, expected_tag: {expected_tag}}}'.format(**kwargs)
        elif id == self.ID_XML_MISSING_TAG:
            self.xtext = id + '{{filepath: {filepath}, xmlpath: {xmlpath}, '\
                              'missing_tag: {missing_tag}}}'.format(**kwargs)
        elif id == self.ID_XML_INVALID_TEXT:
            self.xtext = id + '{{filepath: {filepath}, xmlpath: {xmlpath}, '\
                              'text: {text}}}'.format(**kwargs)
        elif id == self.ID_GUID_NOT_UNIQUE:
            self.xtext = id + '{{filepath: {filepath}, guid_value: {guid_value}}}'.format(**kwargs)
        elif id == self.ID_XML_SYNTAX_ERR:
            self.xtext = id + str(kwargs)
        else:
            self.xtext += id + str(kwargs)
        logger.error(self.xtext)


class DictMdlSaveException(Exception):
    ID_INVALID_DICTMDL = 'GuidIsNone'

    def __init__(self, id: str, *args, **kwargs):
        super().__init__()
        self.xtext = 'NotFilledIn'

class IDictMdlPersistence(ABC):
    """description of class"""

    DEFAULT_DICTMDL_CLASS = DictModel


    def __init__(self, dictmdl: DictModel = None, path: str = None, **kwargs):
        super().__init__(**kwargs)
        self.dictmdl = dictmdl
        self.path = path    

    @property
    def dictmdl(self) -> DictModel:
        return self._dictmdl

    @dictmdl.setter
    def dictmdl(self, value: DictModel) -> None:
        assert (value is None) or isinstance(value, DictModel), 'The dictmdl property of {} class shall have {} type.'\
               .format(self.__class__.__name__, DictModel.__name__)
        self._dictmdl = value


    @property
    def path(self) -> str:
        return self._path

    @path.setter
    def path(self, value: str) -> None:
        assert (value is None) or isinstance(value, str), 'The path property of {} class shall have {} type.'\
               .format(self.__class__.__name__, str.__name__)
        self._path = value


    @abc.abstractmethod
    def save_dict(self) -> None:
        pass

    @abc.abstractmethod
    def load_dict(self) -> DictModel:
        pass

    @abc.abstractmethod
    def to_string(self) -> str:
        pass

    @abc.abstractmethod
    def from_string(self, string: str) -> DictModel:
        pass



class XmlDictMdlPersistence(IDictMdlPersistence):
    
    XML_ROOT_TAG = 'Dictionary'
    XML_WORDCOLL_TAG = 'WordCollection'
    XML_WORD_TAG = 'Word'
    XML_WORDCLASS_TAG = 'WordClass'
    XML_GUID_TAG = 'GUID'
    XML_WORDCLASS_NOUN_TEXT = 'Noun'
    XML_WORD_GER_TAG = 'German'
    XML_WORD_HUN_TAG = 'Hungarian'
    XML_NOUN_GER_ART_TAG = 'Article'
    XML_NOUN_GER_SN_TAG = 'Singular'
    XML_NOUN_GER_PL_TAG = 'Plural'
    XML_WORD_HUN_TEXT_SEP = ';'
    XML_NOUN_GER_ART_DER_TEXT = 'der'
    XML_NOUN_GER_ART_DIE_TEXT = 'die'
    XML_NOUN_GER_ART_DAS_TEXT = 'das'
    XML_NONE_TEXT = '__None__'

    XML_FILE_DEFAULT_CODING = 'UTF-8'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._dictxml = None


    def load_dict(self) -> DictModel:
        self._dictxml = etree.parse(self.path)
        self._load_dict_skeleton()
        self.dictmdl.guid_alloc_en = True


    def from_string(self, string: str) -> DictModel:
        self._dictxml = etree.fromstring(string)
        self._load_dict_skeleton()


    def _load_dict_skeleton(self) -> DictModel:
        if self.dictmdl is None:
            self.dictmdl = IDictMdlPersistence.DEFAULT_DICTMDL_CLASS()
        
        xmlroot = self._dictxml.getroot()
        
        if xmlroot.tag != self.XML_ROOT_TAG:     
            raise DictMdlLoadException(DictMdlLoadException.ID_XML_INVALID_TAG,
                    filepath = self.path, xmlpath = self._dictxml.getelementpath(xmlroot),
                    current_tag = xmlroot.tag, expected_tag = self.XML_ROOT_TAG)

        if len(xmlroot) == 0:
            raise DictMdlLoadException(DictMdlLoadException.ID_XML_MISSING_TAG,
                    filepath = self.path, xmlpath = self._dictxml.getelementpath(xmlroot),
                    missing_tag = self.XML_WORDCOLL_TAG)

        if xmlroot[0].tag != self.XML_WORDCOLL_TAG:
            raise DictMdlLoadException(DictMdlLoadException.ID_XML_INVALID_TAG,
                    filepath = self.path, xmlpath = self._dictxml.getelementpath(xmlroot[0]),
                    current_tag = xmlroot[0].tag, expected_tag = self.XML_WORDCOLL_TAG)
        
        xmlwordcoll = xmlroot[0]
        for xmlword in xmlwordcoll:
            if logger.isEnabledFor(logging.DEBUG):
                logger.debug('XmlParseStage: {} file {}/{}.'.format(self.path,
                                xmlword.tag, self._dictxml.getelementpath(xmlword)))
            if xmlword.tag == self.XML_WORD_TAG:
                self._load_word(xmlword)
            else:
                raise DictMdlLoadException(DictMdlLoadException.ID_XML_INVALID_TAG,
                        filepath = self.path, xmlpath = self._dictxml.getelementpath(xmlword),
                        current_tag = xmlword.tag, expected_tag = self.XML_WORD_TAG)


    def _load_word(self, xmlword: Word) -> Word:
        guid = None
        xmlguid = None
        for element in xmlword:
            if element.tag == self.XML_GUID_TAG:
               xmlguid = element 
               guid = self._parse_guid(element.text)

        if xmlguid is None:
            raise DictMdlLoadException(DictMdlLoadException.ID_XML_MISSING_TAG,
                    filepath = self.path, xmlpath = self._dictxml.getelementpath(xmlword),
                    missing_tag = self.XML_GUID_TAG)
        elif guid is None:
            raise DictMdlLoadException(DictMdlLoadException.ID_XML_INVALID_TEXT,
                    filepath = self.path, xmlpath = self._dictxml.getelementpath(xmlguid),
                    text = xmlguid.text)
        elif guid in self.dictmdl:
            raise DictMdlLoadException(DictMdlLoadException.ID_GUID_NOT_UNIQUE,
                    filepath = self.path, guid_value = guid)

        word = None
        xmlhun = None
        for element in xmlword:
            if element.tag == self.XML_WORDCLASS_TAG:
                if element.text == self.XML_WORDCLASS_NOUN_TEXT:
                    word = self._load_noun(xmlword)
                else:
                    logger.warning('Unknown WordClass "{}" is found at {} in {}.'.format(
                                    element.text, self._dictxml.getelementpath(element), self.path))
            elif element.tag == self.XML_WORD_HUN_TAG:
                xmlhun = element

        if word is not None:
            if xmlhun is not None:
                xmlhunlongtext = element.text
                if xmlhunlongtext is not None:
                    word.hun.update([hunstr.strip() for hunstr in xmlhunlongtext.split(self.XML_WORD_HUN_TEXT_SEP)])
                word.guid = guid
                
            self.dictmdl.add_word(word)
        return word


    def _load_noun(self, xmlword: etree._Element) -> Noun:
        noun = Noun()

        xmlger = None
        for element in xmlword:
            if element.tag == self.XML_WORD_GER_TAG:
                xmlger = element
                xmlarticletext = None
                xmlnounsntext = None
                xmlnounpltext = None

        if xmlger is not None:
            for gersubelement in xmlger:
                if gersubelement.tag == self.XML_NOUN_GER_ART_TAG:
                    xmlarticletext = gersubelement.text
                elif gersubelement.tag == self.XML_NOUN_GER_SN_TAG:
                    xmlnounsntext = gersubelement.text
                elif gersubelement.tag == self.XML_NOUN_GER_PL_TAG:
                    xmlnounpltext = gersubelement.text

            if (xmlnounsntext is not None) and (xmlnounsntext.strip() == self.XML_NONE_TEXT):
                xmlnounsntext = None
                noun.singular_exist = False
            else:
                noun.singular_exist = True
            
            if (xmlnounpltext is not None) and (xmlnounpltext.strip() == self.XML_NONE_TEXT):
                xmlnounpltext = None
                noun.plural_exist = False
            else:
                noun.plural_exist = True

            noun.nounpl = xmlnounpltext
            noun.nounsn = xmlnounsntext

            if xmlarticletext is not None:
                xmlarticletext = xmlarticletext.strip()
                if xmlarticletext == self.XML_NOUN_GER_ART_DER_TEXT:
                    noun.gender = GrammaticalGender.MASCULINE
                elif xmlarticletext == self.XML_NOUN_GER_ART_DIE_TEXT:
                    if noun.singular_exist:
                        noun.gender = GrammaticalGender.FEMININE
                    else:
                        noun.gender = GrammaticalGender.PLURAL
                elif xmlarticletext == self.XML_NOUN_GER_ART_DAS_TEXT:
                    noun.gender = GrammaticalGender.NEUTRAL
                else:
                    noun.gender = None
            else:
                noun.gender = None
        return noun

    
    def _parse_guid(self, guidtext: str) -> int:
        guid = None
        if guidtext is not None:
            guidtext = guidtext.strip()
            try:
                if (len(guidtext) > 2) and (guidtext[0:2] == '0x'):
                    base = 16
                else:
                    base = 10                

                guid = int(guidtext, base)
                
                if guid < 0:
                    guid = None
                    
            except ValueError as ex:
                guid = None

        return guid
        

    def save_dict(self) -> None:
        xmldict = self._save_dict_skeleton()
        xmldict.write(self.path, pretty_print = True, encoding = self.XML_FILE_DEFAULT_CODING)

    def to_string(self) -> str:
        xmldict = self._save_dict_skeleton()
        return etree.tostring(xmldict, pretty_print = True, encoding = self.XML_FILE_DEFAULT_CODING).decode(self.XML_FILE_DEFAULT_CODING)


    def _save_dict_skeleton(self) -> etree._ElementTree:
        if self.dictmdl is None:
            raise ValueError('The dictmdl shall not be None during save.')

        xmlroot = etree.Element(self.XML_ROOT_TAG)
        xmldict = etree.ElementTree(xmlroot)

        xmlwordcoll = etree.SubElement(xmlroot, self.XML_WORDCOLL_TAG)
        wordlist = self.dictmdl.get_wordlist()

        for word in wordlist:
            if (word.guid is None):
                raise ValueError('The guid of Word object shall not be None.')

            xmlword = etree.SubElement(xmlwordcoll, self.XML_WORD_TAG)
            xmlguid = etree.SubElement(xmlword, self.XML_GUID_TAG)
            xmlguid.text = hex(word.guid)
            xmlwordclass = etree.SubElement(xmlword, self.XML_WORDCLASS_TAG)

            if word.get_wordclass() == WordClass.NOUN:
                xmlwordclass.text = self.XML_WORDCLASS_NOUN_TEXT
                xmlger = etree.SubElement(xmlword, self.XML_WORD_GER_TAG)

                xmlarticle = etree.SubElement(xmlger, self.XML_NOUN_GER_ART_TAG)
                
                if word.gender is None:
                    xmlarticle.text = ''
                else:
                    articleenum = Article.get_article(ArticleType.DEFINITE, word.gender, 
                                                      GrammaticalCase.NOMINATIVE)
                    if articleenum == Article.DER:
                        xmlarticle.text = self.XML_NOUN_GER_ART_DER_TEXT
                    elif articleenum == Article.DIE:
                        xmlarticle.text = self.XML_NOUN_GER_ART_DIE_TEXT
                    elif articleenum == Article.DAS:
                        xmlarticle.text = self.XML_NOUN_GER_ART_DAS_TEXT
                    else:
                        xmlarticle.text = ''

                xmlnounsn = etree.SubElement(xmlger, self.XML_NOUN_GER_SN_TAG)
                if word.singular_exist:
                    xmlnounsn.text = '' if word.nounsn is None else word.nounsn
                else:
                    xmlnounsn.text = self.XML_NONE_TEXT

                xmlnounpl = etree.SubElement(xmlger, self.XML_NOUN_GER_PL_TAG)
                if word.plural_exist:
                    xmlnounpl.text = '' if word.nounpl is None else word.nounpl
                else:
                    xmlnounpl.text = self.XML_NONE_TEXT

            xmlhun = etree.SubElement(xmlword, self.XML_WORD_HUN_TAG)
            if word.hun is None:
                xmlhun.text = ''
            else:
                xmlhun.text = self.XML_WORD_HUN_TEXT_SEP.join(word.hun)
        return xmldict
        

# root = etree.Element('Dictionary')
# etree.SubElement(root, 'WordCollection')
# print(etree.tostring(root, pretty_print = True).decode('utf-8'))