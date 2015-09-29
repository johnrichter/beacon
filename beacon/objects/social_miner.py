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

    .. note::

        AngelList allows lookup by URL slug (i.e. the link text a user has chosen for their profile,
        e.g. James Bond could be using slug: james-bond) or MD5 hash of a user's email address.
        Other notable information we can gather is blog_url, online_bio_url, twitter_url,
        facebook_url, linkedin_url, angellist_url, dribble_url, github_url, resume_url,
        profile picture, and full name.  We may be able to parse the bio, what_i_do,
        and what_ive_built fields for email and username information.

    .. note

        LinkedIn

    .. _any API endpoint: https://dev.twitter.com/faq#26
    """
    def __init__(self):
        pass
