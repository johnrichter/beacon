import unittest

# from beacon.db import create_db, destroy_db
from beacon.util.names import (
    retrieve_nicknames_for_name,
    get_fml_name_variations,
    get_fl_name_variations,
)


class TestNameUtils(unittest.TestCase):
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
