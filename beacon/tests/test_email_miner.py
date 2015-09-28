import unittest

from beacon.objects.email_miner import EmailMiner


class TestEmailMiner(unittest.TestCase):
    def setUp(self):
        self.miner = EmailMiner()

    def test_get_email_addresses_with_usernames(self):
        email_addresses = self.miner.get_email_addresses_with_usernames(['jbond'])
        expected_email_addresses = [
            'jbond@aol.com', 'jbond@atmail.com', 'jbond@fastmail.com',
            'jbond@getanemailaddress.info', 'jbond@gmail.com',
            'jbond@gmx.com', 'jbond@gmx.net', 'jbond@gmx.us', 'jbond@hushmail.com',
            'jbond@hushmail.me', 'jbond@hush.com', 'jbond@hush.ai', 'jbond@mac.hush.com',
            'jbond@icloud.com', 'jbond@me.com', 'jbond@lycos.com', 'jbond@mail.com',
            'jbond@email.com', 'jbond@outlook.com', 'jbond@hotmail.com', 'jbond@protonmail.com',
            'jbond@rediffmail.com', 'jbond@runbox.com', 'jbond@yahoo.com', 'jbond@yahdex.com',
            'jbond@zoho.com'
        ]
        self.assertListEqual(sorted(email_addresses), sorted(expected_email_addresses))

    def test_get_email_addresses_with_usernames_with_long_username(self):
        email_addresses = self.miner.get_email_addresses_with_usernames([
            'thisusernameiswaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
            'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
            'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaatoolong'
        ])
        self.assertTrue(len(email_addresses) == 0)

    def test_is_valid_email_domain(self):
        self.assertTrue(self.miner.is_valid_email_domain('gmail.com'))
        self.assertFalse(self.miner.is_valid_email_domain('areallyfakedomainname12312312.com'))
