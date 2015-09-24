import unittest

# from beacon.db import create_db, destroy_db
from beacon.algorithms.names import enumerate_full_name_combinations


class TestNameAlgorithms(unittest.TestCase):
    # @classmethod
    # def setUpClass(cls):
    #     create_db()
    #
    # @classmethod
    # def tearDownClass(cls):
    #     destroy_db()

    def setUp(self):
        self.first_name = 'James'
        self.middle_name = 'Herbert'
        self.last_name = 'Bond'

    def test_enumerate_full_name_combinations_first_last(self):
        generated_names = enumerate_full_name_combinations(self.first_name, self.last_name, '')
        expected_names_subset = ['James Bond', 'Bond James', 'Bond, James']
        for name in expected_names_subset:
            self.assertTrue(name in generated_names)

    def test_enumerate_full_name_combinations_alternate_first_names(self):
        generated_names = enumerate_full_name_combinations(self.first_name, self.last_name)
        expected_names_subset = ['Jim Bond', 'Jimmie Bond', 'Jimmy Bond', 'Jamie Bond']
        for name in expected_names_subset:
            self.assertTrue(name in generated_names)

    def test_enumerate_full_name_combinations_first_middle_last(self):
        generated_names = enumerate_full_name_combinations(
            self.first_name, self.last_name,  self.middle_name
        )
        expected_names_subset = [
            'James Herbert Bond', 'Herbert Bond James', 'Bond James Herbert',
            'James, Herbert, Bond', 'Herbert, Bond, James', 'Bond, James, Herbert',
            'Bond, James Herbert'
        ]
        for name in expected_names_subset:
            self.assertTrue(name in generated_names)

    def test_enumerate_full_name_combinations_first_middle_initial_last(self):
        generated_names = enumerate_full_name_combinations(
            self.first_name, self.last_name, self.middle_name
        )
        expected_names_subset = [
            'James H Bond', 'H Bond James', 'Bond James H',
            'James, H, Bond', 'H, Bond, James', 'Bond, James, H',
            'Bond, James H'
        ]
        for name in expected_names_subset:
            self.assertTrue(name in generated_names)
