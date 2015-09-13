import argparse


__version__ = '0.1'


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
    parser.add_argument('-d', '--domain', action='store', nargs='+',
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
