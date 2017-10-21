from language.langobj import LangObj

class Tag(LangObj):
    """description of class"""
    

    @property
    def tag(self) -> str:
        return self._tag

    @tag.setter
    def tag(self, value: str) -> None:
        assert isinstance(value, str), 'The tag property of {} class shall have {} type.'\
               .format(self.__class__.__name__, str.__name__)
        self._tag = value


    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, value: str) -> None:
        assert isinstance(value, str), 'The description property of {} class shall have {} type.'\
               .format(self.__class__.__name__, str.__name__)
        self._description = value


