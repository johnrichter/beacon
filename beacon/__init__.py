import argparse
import os
import inspect
import json

from beacon.objects.person import Person
from beacon.objects.person_locator import PersonLocator

__version__ = '0.1'
ASSESTS_PATH = os.path.realpath(os.path.join(os.path.dirname(inspect.stack()[0][1]), 'assets'))

# TODO: Move to real DB or fix the way we initialize the DB so it doesn't happen on import
from beacon.db import create_db
create_db()


def parse_arguments():
    parser = argparse.ArgumentParser(description='Locate someone on the internet.')

    # Required arguments
    parser.add_argument('first_name', type=str, action='store',
                        help="The person's first name")
    parser.add_argument('last_name', type=str, action='store',
                        help="The person's last name")

    # Optional arguments
    parser.add_argument('-m', '--middle_name', type=str, action='store',
                        help="The person's middle name")
    parser.add_argument('-d', '--domains', action='store', nargs='+',
                        help='One or more affiliated domains owned or used by or used by the '
                             'person')
    parser.add_argument('-l', '--linkedin_url', type=str, action='store',
                        help="The person's LinkedIn profile URL" )
    parser.add_argument('-a', '--angellist_url', type=str, action='store',
                        help="The person's AngelList profile URL")
    parser.add_argument('-t', '--twitter_url', type=str, action='store',
                        help="The person's Twitter profile URL")

    # Misc
    parser.add_argument('--version', action='version', version=__version__)

    args = parser.parse_args()
    return args


def find_online_presence(first_name, last_name, middle_name=None, domains=None,
                         linkedin_url=None, angellist_url=None, twitter_url=None):
    """
    Discover a single person's online presence, if possible.

    Attempts to find accurate user information from the following services/service types:
    #. Email (Gmail, Outlook, Hotmail, Yahoo)
    #. Web Domains (personal or corporate)
    #. LinkedIn
    #. AngelList
    #. Twitter

    :param first_name: The person's first name
    :param last_name: The person's last name
    :param middle_name: The person's middle name
    :param domains: Domains, personal or corporate, that the person associates with
    :param linkedin_url: The person's profile URL
    :param angellist_url: The person's AngelList URL
    :param twitter_url: The person's Twitter URL
    :return: JSON representation of the person's online presence information
    """

    # Create our person to be found
    hidden_person = Person(
        first_name,
        last_name,
        middle_name,
        domains,
        linkedin_url,
        angellist_url,
        twitter_url
    )

    # Create a locator to find the person
    locator = PersonLocator(hidden_person)

    # Find them. Do whatever it takes (brute_force=True)
    locator.locate(brute_force=True)

    return json.dumps(hidden_person.__dict__)
