from enum import Enum, IntEnum, unique

@unique
class GrammaticalCase(IntEnum):
    NOMINATIVE = 0
    ACCUSATIVE = 1
    DATIVE     = 2
    GENITIVE   = 3

@unique
class GrammaticalGender(IntEnum):
    MASCULINE = 0
    NEUTRAL   = 1
    FEMININE  = 2
    PLURAL    = 3

@unique
class ArticleType(IntEnum):
    DEFINITE   = 0
    INDEFINITE = 1

@unique
class Article(IntEnum):
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

    def get_article(arttype: ArticleType, gender: GrammaticalGender, case: GrammaticalCase) -> 'Article':
        assert isinstance(arttype, ArticleType), 'The arttype parameter of {} method in {} class shall have {} type.'\
               .format(get_article.__name__, self.__class__.__name__, ArticleType.__name__)
        assert isinstance(gender, GrammaticalGender), 'The gender parameter of {} method in {} class shall have {} type.'\
               .format(get_article.__name__, self.__class__.__name__, GrammaticalGender.__name__)
        assert isinstance(case, GrammaticalCase), 'The case parameter of {} method in {} class shall have {} type.'\
               .format(get_article.__name__, self.__class__.__name__, GrammaticalCase.__name__)

        article = None
        if arttype == ArticleType.DEFINITE:
            article = ArticleLookup.DEFINITE_ARTICLE_LOOKUP[case][gender]
        else:
            article = ArticleLookup.INDEFINITE_ARTICLE_LOOKUP[case][gender]
        return article

class ArticleLookup(object):
    
    DEFINITE_ARTICLE_LOOKUP = (
        (Article.DER, Article.DAS, Article.DIE, Article.DIE), # Nominative
        (Article.DEN, Article.DAS, Article.DIE, Article.DIE), # Accusative
        (Article.DEM, Article.DEM, Article.DER, Article.DEN), # Dative
        (Article.DES, Article.DES, Article.DER, Article.DER)  # Genitive
    )

    INDEFINITE_ARTICLE_LOOKUP = (
        (Article.EIN,   Article.EIN,   Article.EINE, None),  # Nominative
        (Article.EINEN, Article.EIN,   Article.EINE, None),  # Accusative
        (Article.EINEM, Article.EINEM, Article.EINER, None), # Dative
        (Article.EINES, Article.EINES, Article.EINER, None)  # Genitive
    )