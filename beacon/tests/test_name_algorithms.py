import unittest

# from beacon.db import create_db, destroy_db
from beacon.algorithms.names import (
    enumerate_full_name_combinations,
    retrieve_nicknames_for_name,
    get_fml_name_variations,
    get_fl_name_variations,
    determine_probable_usernames_for_full_name
)


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

    def test_retrieve_nicknames_for_name_with_successful_name(self):
        """
        Can retrieve nicknames for a name that we know has nicknames?
        """
        generated_names = retrieve_nicknames_for_name(self.first_name)
        generated_names.sort()
        expected_names = ['Jim', 'Jimmie', 'Jimmy', 'Jamie']
        expected_names.sort()
        self.assertListEqual(generated_names, expected_names)

    def test_retrieve_nicknames_for_name_with_fake_name(self):
        """
        Do we receive an empty list for a name without nicknames?
        """
        generated_names = retrieve_nicknames_for_name('abcdefg')
        self.assertListEqual(generated_names, [])

    def test_enumerate_full_name_combinations_first_last(self):
        """
        Are simple combinations of first and last names generated?
        """
        generated_names = enumerate_full_name_combinations(self.first_name, self.last_name, '')
        expected_names_subset = ['James Bond', 'Bond James', 'Bond, James']
        for name in expected_names_subset:
            self.assertTrue(name in generated_names)

    def test_enumerate_full_name_combinations_alternate_first_names(self):
        """
        Are the simple combinations of first and last name containing alternate first names
        generated?
        """
        generated_names = enumerate_full_name_combinations(self.first_name, self.last_name)
        expected_names_subset = ['Jim Bond', 'Jimmie Bond', 'Jimmy Bond', 'Jamie Bond']
        for name in expected_names_subset:
            self.assertTrue(name in generated_names)

    def test_enumerate_full_name_combinations_first_middle_last(self):
        """
        Are a sampling of the complex combinations of first, middle, and last names generated?
        :return:
        """
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
        """
        Are a sample of complex combinations of first, middle, middle initial, and last names
        generated?
        """
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

    def test_get_fml_username_variations(self):
        """
        Are all of the first, middle, and last name variations generated, including initials?
        """
        generated_usernames = get_fml_name_variations(
            self.first_name, self.middle_name, self.last_name, True
        )
        generated_usernames.sort()
        expected_usernames = [
            ('James', 'Herbert', 'Bond'), ('J', 'Herbert', 'Bond'), ('James', 'H', 'Bond'),
            ('James', 'Herbert', 'B'), ('J', 'H', 'Bond'), ('J', 'Herbert', 'B'),
            ('James', 'H', 'B'), ('J', 'H', 'B')
        ]
        expected_usernames.sort()
        self.assertListEqual(generated_usernames, expected_usernames)

    def test_get_fl_username_variations(self):
        """
        Are all of hte first and last name variations generated, including initials?
        :return:
        """
        generated_usernames = get_fl_name_variations(
            self.first_name, self.last_name, True
        )
        generated_usernames.sort()
        expected_usernames = [
            ('James', 'Bond'), ('J', 'Bond'), ('James', 'B'), ('J', 'B')
        ]
        expected_usernames.sort()
        self.assertListEqual(generated_usernames, expected_usernames)

    def test_determine_probable_usernames_for_full_name(self):
        """
        Are a subset of username combinations and a subset of name/symbol combinations generated?
        :return:
        """
        generated_usernames = determine_probable_usernames_for_full_name(
            self.first_name, self.last_name, self.middle_name
        )
        expected_usernames_subset = [
            'JamesBond', 'James.Bond', 'James_Bond', 'J.Bond', 'J.B', 'James.B', 'James_B',
            'BondJames', 'BJames', 'B_James', 'JamesHerbertBond', 'JHerbertBond', 'J.HerbertBond',
            'J_HerbertBond', 'JHerbert.Bond', 'JHerbert_Bond', 'Bond_James.H', 'BJH', 'J.H.B',
            'James_H_Bond', 'Bond.J_Herbert'
        ]
        for username in expected_usernames_subset:
            self.assertTrue(username in generated_usernames)

        # Names in the order of `Last Middle First` should not be generated
        self.assertTrue('BondHerbertJames' not in generated_usernames)

        # Usernames should not start or end with special characters
        for username in generated_usernames:
            self.assertFalse(username.startswith('.'))
            self.assertFalse(username.startswith('_'))
            self.assertFalse(username.endswith('.'))
            self.assertFalse(username.endswith('_'))
