import unittest

from beacon.objects.email_miner import EmailMiner


class TestEmailMiner(unittest.TestCase):
    def setUp(self):
        self.miner = EmailMiner()

