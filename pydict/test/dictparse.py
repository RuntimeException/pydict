import unittest
from lxml import etree

class Test_DictParse(unittest.TestCase):
    
    def test_dict_lxmlopen(self):
        dictxml = etree.parse(r'dict.xml')

    def test_dict_iter(self):
        dictxml = etree.parse(r'dict.xml')
        dictel = dictxml.getroot()
        self.assertEqual(dictel.tag, 'Dictionary')
        wordcollel = None
        for element in dictel:
            if element.tag == 'WordCollection':
                wordcollel = element
        self.assertIsNotNone(wordcollel)


if __name__ == '__main__':
    unittest.main()
