from beacon.db.models import Name
from beacon.db import db_connect


class Person(object):
    """
    An object to represent a person and their online presence.
    """
    def __init__(self, first_name, last_name, middle_name=None, domains=None, linkedin_url=None,
                 angellist_url=None, twitter_url=None):
        self.first_name = first_name.capitalize()
        self.last_name = last_name.capitalize()
        self.middle_name = middle_name.capitalize() if middle_name else ""
        self.domains = domains if domains else []
        self.linkedin_url = linkedin_url if linkedin_url else ""
        self.angellist_url = angellist_url if angellist_url else ""
        self.twitter_url = twitter_url if twitter_url else ""

        self.probable_usernames = []
        self.probable_email_addresses = []

    def _determine_probable_usernames(self):
        pass

    def _discover_probable_email_addresses(self):
        pass

    def locate(self):
        # Enumerate each way our person's full name can be represented
        self._enumerate_full_name_combinations()

        # Determine the usernames the person is most likely to use based on their full name and
        # their LinkedIn, AngelList, and Twitter URLs
        self._determine_probable_usernames()

        # Discover email addresses on popular email services with the person's probable usernames
        self._discover_probable_email_addresses()

    def has_middle_name(self):
        return len(self.middle_name) > 0
