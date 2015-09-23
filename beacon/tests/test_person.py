import unittest

from beacon.objects.person import Person
from beacon.db import create_db, destroy_db

class TestPersonMethods(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        create_db()

    @classmethod
    def tearDownClass(cls):
        destroy_db()

    def setUp(self):
        self.person = Person('James', 'Bond')

    def tearDown(self):
        pass

    def test_enumerate_full_name_combinations_first_last(self):
        self.person._enumerate_full_name_combinations()
        expected_names = ['James Bond', 'Bond James', 'Bond, James']
        for name in expected_names:
            self.assertTrue(name in self.person.full_name_variants)

    def test_enumerate_full_name_combinations_first_middle_last(self):
        self.person.middle_name = 'Herbert'
        self.person._enumerate_full_name_combinations()

        expected_names = [
            'James Herbert Bond', 'Herbert Bond James', 'Bond James Herbert',
            'James, Herbert, Bond', 'Herbert, Bond, James', 'Bond, James, Herbert',
            'Bond, James Herbert'
        ]
        for name in expected_names:
            self.assertTrue(name in self.person.full_name_variants)

    def test_enumerate_full_name_combinations_first_middle_initial_last(self):
        self.person.middle_name = 'Herbert'
        self.person._enumerate_full_name_combinations()

        expected_names = [
            'James H Bond', 'H Bond James', 'Bond James H',
            'James, H, Bond', 'H, Bond, James', 'Bond, James, H',
            'Bond, James H'
        ]
        for name in expected_names:
            self.assertTrue(name in self.person.full_name_variants)

    def test_enumerate_full_name_combinations_alternate_first_names(self):
        self.person._enumerate_full_name_combinations()
        expected_names = ['Jim Bond', 'Jimmie Bond', 'Jimmy Bond', 'Jamie Bond']
        for name in expected_names:
            self.assertTrue(name in self.person.full_name_variants)

    @unittest.skip('Not Implemented')
    def test_determine_probable_usernames(self):
        pass

    @unittest.skip('Not Implemented')
    def test_discover_probable_email_addresses(self):
        pass

