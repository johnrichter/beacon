class SocialMiner(object):
    """
    An object to search LinkedIn, AngelList, and Twitter for accounts matching certain usernames
    and email addresses and gathering account information about that individual.

    .. note::

        Twitter does not support *obtaining* or *searching for* email addresses from **`any API
        endpoint`_**. However may be able to parse the user's own description for email addresses.
        It may be possible to use the 'import my contacts' feature somehow to get around this
        limitation. Other notable information we can gather is the user's name, profile picture,
        and banner picture.

    .. _any API endpoint: https://dev.twitter.com/faq#26
    """
    def __init__(self):
        pass
