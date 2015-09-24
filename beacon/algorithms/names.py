
from beacon.db import db_connect
from beacon.db.models import Name


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
    first_names = [first_name]
    with db_connect() as session:
        # Look for the first_name in the database and append all nicknames to our fist_name list
        db_name = session.query(Name).filter_by(real_name=first_name).first()
        if db_name:
            for nick in db_name.nick_names:
                first_names.append(nick.real_name)

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
