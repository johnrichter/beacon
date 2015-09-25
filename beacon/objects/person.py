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
        self.usernames = {}

        if twitter_url:
            self.twitter_url = twitter_url
            self.usernames['twitter'] = [wd for wd in twitter_url.split('/') if wd != ''][-1]
        else:
            self.twitter_url = ""

    def has_middle_name(self):
        """
        Determine if a `Person` has a middle name
        """
        return len(self.middle_name) > 0
