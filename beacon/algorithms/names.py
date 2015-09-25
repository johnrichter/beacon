import unicodedata

from beacon.db import db_connect
from beacon.db.models import Name


def retrieve_nicknames_for_name(name):
    """
    Retrieve nicknames for `name` from the database

    :param name: The name that might have nicknames
    :return: A list of nicknames.  Empty list if nicknames were not found.
    """
    nick_names = []
    with db_connect() as session:
        # Look for the name in the database and append all nicknames to our nick_names list
        db_name = session.query(Name).filter_by(real_name=name).first()
        if db_name:
            for nick in db_name.nick_names:
                nick_names.append(nick.real_name)

    return nick_names


def enumerate_full_name_combinations(first_name, last_name, middle_name=None):
    """
    Enumerate a person's full name in the common ways full names can be represented.
    Includes common nicknames for the person's first name and middle name/initial when the
    person has a middle name.  Full names generated are intended to be compared to
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

    .. TODO: Migrate to use the `get_[f]ml_name_variations()` functions

    :return: A frozenset() of all full names
    """
    fml_patterns = [
        '{f} {m} {l}',   '{m} {l} {f}',   '{l} {f} {m}',
        '{f}, {m}, {l}', '{m}, {l}, {f}', '{l}, {f}, {m}',
        '{l}, {f} {m}'
    ]
    fl_patterns = ['{f} {l}', '{l} {f}', '{l}, {f}']
    first_name = first_name.title()
    last_name = last_name.title()
    have_middle_name = len(middle_name) > 0 if middle_name else False
    if have_middle_name:
        middle_name = middle_name.title()

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
        for pattern in fml_patterns if have_middle_name else []:
            generated_names.add(pattern.format(f=first, m=middle_name, l=last_name))
            generated_names.add(pattern.format(f=first, m=middle_name[0], l=last_name))

    return frozenset(generated_names)


def get_fml_name_variations(first_name, middle_name, last_name, include_initials=False):
    """
    Generate different variations of a full name containing the first, middle, last name.

    :param first_name: The first name
    :param middle_name: The middle name
    :param last_name: The last name
    :param include_initials: Include variations with names abbreviated by their first letter
    :return: A list of (first_name, middle_name, last_name) tuples
    """
    variations = [(first_name, middle_name, last_name)]
    if include_initials:
        variations.extend([
            (first_name[0], middle_name, last_name),
            (first_name, middle_name[0], last_name),
            (first_name, middle_name, last_name[0]),
            (first_name[0], middle_name[0], last_name),
            (first_name[0], middle_name, last_name[0]),
            (first_name, middle_name[0], last_name[0]),
            (first_name[0], middle_name[0], last_name[0])
        ])

    return variations


def get_fl_name_variations(first_name, last_name, include_initials=False):
    """
    Generate different variations of a full name containing only the first and last name.

    :param first_name: The first name
    :param last_name: The last name
    :param include_initials: Include variations with names abbreviated by their first letter
    :return: A list of (first_name, last_name) tuples
    """
    variations = [(first_name, last_name)]
    if include_initials:
        variations.extend([
            (first_name[0], last_name), (first_name, last_name[0]), (first_name[0], last_name[0])
        ])

    return variations


def determine_probable_usernames_for_full_name(first_name, last_name, middle_name=None):
    """
    Build a simple list of user names based on a person's full name.

    Limit our formatting to only the special symbols in ``._`` and alphanumeric characters in
    ``a-zA-Z0-9``.  Usernames of services such as Gmail, Yahoo, Outlook.com, LinkedIn, AngelList,
    and Twitter are restricted to these characters despite RFCs allowing more characters (
    including unicode in some cases).

    Email: `RFC 3696`_

    .. _RFC 3696: https://tools.ietf.org/html/rfc3696

    .. TODO:
    .. * Expand our guesses to include numbers once we obtain age, birthday, etc
    .. * Translate non-latin characters to their latin equivalent
    .. *

    :param first_name: The first name
    :param last_name: The last name
    :param middle_name: The middle name
    :return: A list of user names
    """

    fml_pattern = '{f}{s1}{m}{s2}{l}'
    common_special_characters = ['.', '_', '']
    name_variations = []
    generated_usernames = []
    have_middle_name = len(middle_name) > 0 if middle_name else False

    # Normalize characters in each name to their decomposed equivalents
    first_name = ''.join([
        c for c in unicodedata.normalize('NFKD', first_name) if not unicodedata.combining(c)
    ])
    last_name = ''.join([
        c for c in unicodedata.normalize('NFKD', last_name) if not unicodedata.combining(c)
    ])
    middle_name = ''.join([
        c for c in unicodedata.normalize('NFKD', middle_name) if not unicodedata.combining(c)
    ]) if have_middle_name else None

    # Build a list of name variations. E.g. (James, Bond), (J, Bond), or (J, H, Bond)
    if have_middle_name:
        name_variations.extend(get_fml_name_variations(first_name, middle_name, last_name, True))
        name_variations.extend(get_fml_name_variations(last_name, first_name, middle_name, True))
        name_variations.extend(get_fml_name_variations(middle_name, last_name, first_name, True))

    name_variations.extend(get_fl_name_variations(first_name, last_name, True))
    name_variations.extend(get_fl_name_variations(last_name, first_name, True))

    # Each variation is a potential username. E.g. JamesBond, JBond, or JHBond
    for name in name_variations:
        generated_usernames.append(''.join(name))

        # Each part of the name can be separated by a special character
        for symbol in common_special_characters:
            if len(name) == 2:      # First and Last
                generated_usernames.append(symbol.join(name))
            elif len(name) == 3:    # First, Middle, and Last
                first, middle, last = name
                # We can have combinations of two symbols separating the names
                for symbol2 in common_special_characters:
                    generated_usernames.append(
                        fml_pattern.format(f=first, m=middle, l=last, s1=symbol, s2=symbol2)
                    )

    return generated_usernames
