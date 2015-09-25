import unicodedata

from beacon.util.names import (
    retrieve_nicknames_for_name,
    get_fl_name_variations,
    get_fml_name_variations
)


class PersonLocator(object):
    """
    An object used to locate the online presence of an individual.
    """
    def __init__(self, person):
        self.person = person
        self.full_name_representations = set()
        self.known_usernames = set()

        self._enumerate_full_name_representations()

    def _enumerate_full_name_representations(self):
        """
        Enumerate a person's full name in the common ways full names can be represented.
        Includes common nicknames for the person's first name and middle name/initial when the
        person has a middle name.  Full names generated are intended to be compared to
        full names obtained from API services, email servers, etc.

        For example:
        Variants of *James Herbert Bond* include, but aren't limited to the following:

        * James Bond
        * Bond James
        * James Herbert Bond
        * James H Bond
        * Jimmy Bond
        * Bond, James
        * Bond, James Herbert
        * Bond, Jim Herbert

        .. todo::
            * Migrate to use the `get_[f]ml_name_variations()` functions.
            * Remove some of the noise via nickname probability mappings

        :return: None
        """
        fml_patterns = [
            '{f} {m} {l}',   '{m} {l} {f}',   '{l} {f} {m}',
            '{f}, {m}, {l}', '{m}, {l}, {f}', '{l}, {f}, {m}',
            '{l}, {f} {m}'
        ]
        fl_patterns = ['{f} {l}', '{l} {f}', '{l}, {f}']
        first_name, middle_name, last_name = self.person.first_name, None, self.person.last_name
        if self.person.has_middle_name():
            middle_name = self.person.middle_name

        # TODO: Remove some of the noise via nickname probability mappings
        # Build a list of potential first names. E.g. Robert > Bob or Johnathan > John > Jon
        nick_names = retrieve_nicknames_for_name(first_name)
        first_names = [first_name]
        first_names.extend(nick_names)

        # Generate our list of potential full name variants
        generated_names = set()
        for first in first_names:
            # Add full first/last name variants
            for pattern in fl_patterns:
                generated_names.add(pattern.format(f=first, l=last_name))

            # Add full first/middle/last name variants, including middle initial variants
            for pattern in fml_patterns if middle_name else []:
                generated_names.add(pattern.format(f=first, m=middle_name, l=last_name))
                generated_names.add(pattern.format(f=first, m=middle_name[0], l=last_name))

        self.full_name_representations = generated_names

    def _enumerate_probable_usernames(self):
        """
        Build a simple list of user names based on a person's full name.

        Limit our formatting to only the special symbols in ``._`` and alphanumeric characters in
        ``a-zA-Z0-9``.  Usernames of services such as Gmail, Yahoo, Outlook.com, LinkedIn, AngelList,
        and Twitter are restricted to these characters despite RFCs allowing more characters (
        including unicode in some cases).

        Email: `RFC 3696`_

        .. _RFC 3696: https://tools.ietf.org/html/rfc3696

        .. todo::
            * Expand our variations to include numbers once we obtain age, birthday, etc
            * Translate non-latin characters to their latin equivalent

        :return: None
        """

        fml_pattern = '{f}{s1}{m}{s2}{l}'
        common_special_characters = ['.', '_', '']  # '' To represent *no special character*
        name_variations = []
        generated_usernames = set()

        # Normalize characters in each name to their decomposed equivalents
        first_name = ''.join([
            c for c in unicodedata.normalize('NFKD', self.person.first_name)
            if not unicodedata.combining(c)
         ])
        middle_name = ''.join([
            c for c in unicodedata.normalize('NFKD', self.person.middle_name)
            if not unicodedata.combining(c)
        ]) if self.person.has_middle_name() else None
        last_name = ''.join([
            c for c in unicodedata.normalize('NFKD', self.person.last_name)
            if not unicodedata.combining(c)
        ])

        # Build a list of name variations. E.g. (James, Bond), (J, Bond), or (J, H, Bond)
        if middle_name:
            name_variations.extend(get_fml_name_variations(first_name, middle_name, last_name, True))
            name_variations.extend(get_fml_name_variations(last_name, first_name, middle_name, True))
            name_variations.extend(get_fml_name_variations(middle_name, last_name, first_name, True))

        name_variations.extend(get_fl_name_variations(first_name, last_name, True))
        name_variations.extend(get_fl_name_variations(last_name, first_name, True))

        # Generate names by concatenating them together with combinations of the special symbols
        for name in name_variations:
            # Each part of the name can be separated by a special character
            for symbol in common_special_characters:
                if len(name) == 2:      # First and Last
                    generated_usernames.add(symbol.join(name))
                elif len(name) == 3:    # First, Middle, and Last
                    first, middle, last = name
                    # We can have combinations of two symbols separating the names
                    for symbol2 in common_special_characters:
                        generated_usernames.add(
                            fml_pattern.format(f=first, m=middle, l=last, s1=symbol, s2=symbol2)
                        )

        self.probable_usernames = generated_usernames

    def _determine_usernames_from_urls(self):
        """
        Mine the person's URLs and save any usernames found.  Modifies a dictionary of services
        to usernames on the person object.

        .. code-block:: python

            {
                'LinkedIn: ['a_username'],
                'AngelList: ['a_username'],
                'Twitter': ['a_different_username'],
            }

        :return: None
        """
        if self.person.linkedin_url:
            # self.person.usernames['linkedin'] = linkedin_username
            pass
        if self.person.angellist_url:
            pass
        if self.person.twitter_url:
            pass

    def _mine_personal_information_from_social_services(self, email_addresses=None):
        """
        Mine the all social services for personal information.  Use the person's existing
        username dictionary if ``email_address`` is None

        :param email_addresses: Email addresses to search for on each service
        :return: A dict() of information type to information objects:
                 {'email_address': ['example@gmail.com']}
        """
        # TODO: Ensure that the first run of SocialMiner, it returns all usernames even though
        # TODO: they were put in the person.usernames dict() before the first call.
        return {}

    def _discover_email_addresses_with_usernames(self, usernames):
        """
        Discover valid email addresses using only the usernames in ``usernames``.

        :param usernames: The usernames to use when discovering new email addresses
        :return: A list of new email addresses
        """
        return []

    def _locate_brute_force(self):
        """
        Bluntly search for our person on the world wide web.

        #. Generate a set of likely usernames minus any usernames already searched for
        #. While we can obtain new usernames and email addresses.
            #. Find valid email addresses that report the same full name as our person
            #. If we were unable to find a user on one of the social services, use the new email
               addresses to attempt to find a user on that service

        Updates ``self.person`` with the most accurate information we can locate

        .. warning::
            Can result in thousands of API calls to LinkedIn, AngelList, Twitter,
            etc. Use with caution when searching for lots of people simultaneously.

        :return: None
        """
        # Generate a list of possible usernames the user could have
        self._enumerate_probable_usernames()

        # Remove already attempted usernames from our generated list
        for service, usernames in self.person.usernames:
            for user in usernames:
                self.probable_usernames.remove(user)

        # Discover valid email addresses that match our person's name
        new_email_addresses = self._discover_email_addresses_with_usernames(
            self.probable_usernames
        )

        while len(new_email_addresses) > 0:
            # Use the new email addresses to find missing usernames/profile URLs
            new_information = self._mine_personal_information_from_social_services(
                email_addresses=new_email_addresses
            )

            # Use any new usernames found from the social services to find new email addresses
            if len(new_information.get('usernames')) > 0:
                new_email_addresses = self._discover_email_addresses_with_usernames(
                    new_information.get('usernames')
                )
            else:
                new_email_addresses = []

    def locate(self, brute_force=False):
        """
        Intelligently search for our person on the world wide web.  Only brute force if necessary

        #. Use the usernames we parsed from the profile URLs to contact all Social Services
        #. While we can obtain new usernames and email addresses
            #. Use the same usernames, along with email addresses obtained from the Social Services
               to discover new email addresses
            #. If we were unable to find a user on one of the social services, use the new email
               addresses to attempt to find a user on that service
        #. If we still don't have any email addresses or social service URLs brute force locate

        Updates ``self.person`` with the most accurate information we can locate

        .. warning::
            ``brute_force`` can result in thousands of API calls to LinkedIn, AngelList, Twitter,
            etc. Use with caution when searching for lots of people simultaneously.

        :param brute_force: Attempt to brute force usernames, email addresses, and social profiles
        :return: None
        """
        # Determine any known usernames from a person's urls
        self._determine_usernames_from_urls()

        # Using the usernames we know are correct, gather information from the social services
        new_information = self._mine_personal_information_from_social_services()

        # Continuously loop until we can't find any new email addresses, usernames, or social URLs
        while len(new_information) > 0:
            # Use any new usernames found mined from the social services to find new email addresses
            new_email_addresses = self._discover_email_addresses_with_usernames(
                new_information['usernames']
            )

            if len(new_email_addresses) > 0:
                # Use the new email addresses to find missing usernames/profile URLs
                new_information = self._mine_personal_information_from_social_services(
                    email_addresses=new_email_addresses
                )
            else:
                new_information = {}

        # If we *still* don't have all of our social URLs or email addresses... Engage BEAST MODE.
        if brute_force:
            self._locate_brute_force()
