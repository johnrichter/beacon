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

        self.full_name_variants = frozenset()
        self.probable_usernames = []
        self.probable_email_addresses = []

    def _has_middle_name(self):
        return len(self.middle_name) > 0

    def _enumerate_full_name_combinations(self):
        """
        Enumerate the person's full name in the common ways full names can be represented.
        Includes common nicknames for the person's first name and middle name/initial when the
        person has a middle name.  Full names generated are intended to be used to compare to
        full names obtained from API services, email servers, etc.

        For example::
        Variants of *James Herbert Bond* include, but aren't limited to the following
            * James Bond
            * Bond James
            * James Herbert Bond
            * James H Bond
            * Jimmy Bond
            * Bond, James
            * Bond, James Herbert
            * Bond, Jim Herbert

        :return: None
        """
        fml_patterns = [
            '{f} {m} {l}',   '{m} {l} {f}',   '{l} {f} {m}',
            '{f}, {m}, {l}', '{m}, {l}, {f}', '{l}, {f}, {m}',
            '{l}, {f} {m}'
        ]
        fl_patterns = ['{f} {l}', '{l} {f}', '{l}, {f}']

        # TODO: Remove some of the noise via nickname probability mappings
        # Build a list of potential first names. E.g. Robert > Bob or Johnathan > John > Jon
        first_names = [self.first_name]
        with db_connect() as session:
            db_name = session.query(Name).filter_by(real_name=self.first_name).first()
            if db_name:
                for nick in db_name.nick_names:
                    first_names.append(nick.real_name)

        # Generate our list of potential full name variants
        generated_names = set()
        for first in first_names:
            middle = self.middle_name if self._has_middle_name() else None
            last = self.last_name

            # Add full first/last name variants
            for pattern in fl_patterns:
                generated_names.add(pattern.format(f=first, l=last))

            # Add full first/middle/last name variants, including middle initial variants
            for pattern in fml_patterns if middle else []:
                generated_names.add(pattern.format(f=first, m=middle, l=last))
                generated_names.add(pattern.format(f=first, m=middle[0], l=last))

        self.full_name_variants = frozenset(generated_names)

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
