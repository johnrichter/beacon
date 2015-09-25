import unittest

from beacon.objects.person import Person
from beacon.objects.person_locator import PersonLocator


class TestPersonLocator(unittest.TestCase):
    def setUp(self):
        self.locator = PersonLocator(Person('James', 'Bond', 'Herbert'))

    def test_enumerate_full_name_combinations_first_last(self):
        """
        Are simple combinations of first and last names generated?
        """
        self.locator._enumerate_full_name_representations()
        expected_names_subset = ['James Bond', 'Bond James', 'Bond, James']
        for name in expected_names_subset:
            self.assertTrue(name in self.locator.full_name_representations)

    def test_enumerate_full_name_combinations_alternate_first_names(self):
        """
        Are the simple combinations of first and last name containing alternate first names
        generated?
        """
        self.locator._enumerate_full_name_representations()
        expected_names_subset = ['Jim Bond', 'Jimmie Bond', 'Jimmy Bond', 'Jamie Bond']
        for name in expected_names_subset:
            self.assertTrue(name in self.locator.full_name_representations)

    def test_enumerate_full_name_combinations_first_middle_last(self):
        """
        Are a sampling of the complex combinations of first, middle, and last names generated?
        """
        self.locator._enumerate_full_name_representations()
        expected_names_subset = [
            'James Herbert Bond', 'Herbert Bond James', 'Bond James Herbert',
            'James, Herbert, Bond', 'Herbert, Bond, James', 'Bond, James, Herbert',
            'Bond, James Herbert'
        ]
        for name in expected_names_subset:
            self.assertTrue(name in self.locator.full_name_representations)

    def test_enumerate_full_name_combinations_first_middle_initial_last(self):
        """
        Are a sample of complex combinations of first, middle, middle initial, and last names
        generated?
        """
        self.locator._enumerate_full_name_representations()
        expected_names_subset = [
            'James H Bond', 'H Bond James', 'Bond James H',
            'James, H, Bond', 'H, Bond, James', 'Bond, James, H',
            'Bond, James H'
        ]
        for name in expected_names_subset:
            self.assertTrue(name in self.locator.full_name_representations)

    def test_determine_probable_usernames_for_full_name(self):
        """
        Are a subset of username combinations and a subset of name/symbol combinations generated?
        """
        self.locator._enumerate_probable_usernames()
        expected_usernames_subset = [
            'JamesBond', 'James.Bond', 'James_Bond', 'J.Bond', 'J.B', 'James.B', 'James_B',
            'BondJames', 'BJames', 'B_James', 'JamesHerbertBond', 'JHerbertBond', 'J.HerbertBond',
            'J_HerbertBond', 'JHerbert.Bond', 'JHerbert_Bond', 'Bond_James.H', 'BJH', 'J.H.B',
            'James_H_Bond', 'Bond.J_Herbert'
        ]
        for username in expected_usernames_subset:
            self.assertTrue(username in self.locator.probable_usernames)

        # Names in the order of `Last Middle First` should not be generated
        self.assertTrue('BondHerbertJames' not in self.locator.probable_usernames)

        # Usernames should not start or end with special characters
        for username in self.locator.probable_usernames:
            self.assertFalse(username.startswith('.'))
            self.assertFalse(username.startswith('_'))
            self.assertFalse(username.endswith('.'))
            self.assertFalse(username.endswith('_'))
