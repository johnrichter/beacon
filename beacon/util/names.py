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


def get_fml_name_variations(first_name, middle_name, last_name, include_initials=False):
    """
    Generate different variations of a full name containing the first, middle, and last name.

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



