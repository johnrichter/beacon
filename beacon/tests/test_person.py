import unittest

from beacon.objects.person import Person


class TestPersonMethods(unittest.TestCase):
    def setUp(self):
        self.person = Person('James', 'Bond', twitter_url='https://twitter.com/jamesbond')

    def test_has_middle_name(self):
        self.assertFalse(self.person.has_middle_name())
        self.person = Person('James', 'Bond', 'Herbert')
        self.assertTrue(self.person.has_middle_name())

