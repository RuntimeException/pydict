from word import Word, WordClass

class Noun(Word):
    """description of class"""
    
    def get_wordclass(self):
        return WordClass.NOUN

    @property
    def gender(self) -> GrammaticalGender:
        return self._gender

    @gender.setter
    def gender(self, value: GrammaticalGender) -> None:
        assert isinstance(value, GrammaticalGender), 'The gender property of {} class shall have {} type.'\
               .format(self.__class__.__name__, GrammaticalGender.__name__)
        self._gender = value

    @property
    def singular_exist(self) -> bool:
        return self._singular_exist

    @singular_exist.setter
    def singular_exist(self, value: bool) -> None:
        assert isinstance(value, bool), 'The singular_exist property of {} class shall have {} type.'\
               .format(self.__class__.__name__, bool.__name__)
        self._singular_exist = value
    
    @property
    def nounsn(self) -> str:
        return self._nounsn

    @nounsn.setter
    def nounsn(self, value: str) -> None:
        assert isinstance(value, str), 'The nounsn property of {} class shall have {} type.'\
               .format(self.__class__.__name__, str.__name__)
        self._nounsn = value

    @property
    def nounpl(self) -> str:
        return self._nounpl

    @nounpl.setter
    def nounpl(self, value: str) -> None:
        assert isinstance(value, str), 'The nounpl property of {} class shall have {} type.'\
               .format(self.__class__.__name__, str.__name__)
        self._nounpl = value

