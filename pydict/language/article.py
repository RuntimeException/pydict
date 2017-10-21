from enum import Enum, unique

@unique
class GrammaticalCase(Enum):
    NOMINATIVE = 0
    ACCUSATIVE = 1
    DATIVE     = 2
    GENITIVE   = 3

@unique
class GrammaticalGender(Enum):
    MASCULINE = 0
    NEUTRAL   = 1
    FEMININE  = 2
    PLURAL    = 3

@unique
class ArticleType(Enum):
    DEFINITE   = 0
    INDEFINITE = 1

@unique
class Article(Enum):
    DER = 0
    DAS = 1
    DIE = 2
    DEN = 3
    DEM = 4
    DES = 5
    EIN = 6
    EINE = 7
    EINEN = 8
    EINEM = 9
    EINER = 10
    EINES = 11

    DEFINITE_ARTICLE_LOOKUP = (
        (DER, DAS, DIE, DIE), # Nominative
        (DEN, DAS, DIE, DIE), # Accusative
        (DEM, DEM, DER, DEN), # Dative
        (DES, DES, DER, DER)  # Genitive
    )

    INDEFINITE_ARTICLE_LOOKUP = (
        (EIN,   EIN,   EINE, None),  # Nominative
        (EINEN, EIN,   EINE, None),  # Accusative
        (EINEM, EINEM, EINER, None), # Dative
        (EINES, EINES, EINER, None)  # Genitive
    )

    def get_article(arttype: ArticleType, gender: GrammaticalGender, case: GrammaticalCase) -> 'Article':
        assert isinstance(arttype, ArticleType), 'The arttype parameter of {} method in {} class shall have {} type.'\
               .format(get_article.__name__, self.__class__.__name__, ArticleType.__name__)
        assert isinstance(gender, GrammaticalGender), 'The gender parameter of {} method in {} class shall have {} type.'\
               .format(get_article.__name__, self.__class__.__name__, GrammaticalGender.__name__)
        assert isinstance(case, GrammaticalCase), 'The case parameter of {} method in {} class shall have {} type.'\
               .format(get_article.__name__, self.__class__.__name__, GrammaticalCase.__name__)

        article = None
        if arttype == ArticleType.DEFINITE:
            article = DEFINITE_ARTICLE_LOOKUP[case][gender]
        else:
            article = INDEFINITE_ARTICLE_LOOKUP[case][gender]
        return article

