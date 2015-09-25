import unittest

from beacon.objects.social_miner import SocialMiner


class TestEmailMiner(unittest.TestCase):
    def setUp(self):
        self.miner = SocialMiner()

