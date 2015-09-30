class SocialMiner(object):
    """
    An object to search LinkedIn, AngelList, and Twitter for accounts matching certain usernames
    and email addresses and gathering account information about that individual.

    .. note::

        Twitter does not support *obtaining* or *searching for* email addresses from **`any API
        endpoint`_**. However may be able to parse the user's own description for email addresses.
        It may be possible to use the *import my contacts* feature somehow to get around this
        limitation. Other notable information we can gather is the user's name, profile picture,
        and banner picture.

    .. note::

        AngelList allows lookup by URL slug (i.e. the link text a user has chosen for their profile,
        e.g. James Bond could be using slug: james-bond) or MD5 hash of a user's email address.
        Other notable information we can gather is blog_url, online_bio_url, twitter_url,
        facebook_url, linkedin_url, angellist_url, dribble_url, github_url, resume_url,
        profile picture, and full name.  We may be able to parse the bio, what_i_do
        and what_ive_built, for email and username information.

    .. note::

        LinkedIn, for privacy and security reasons, has locked down on their API and doesn't allow
        searching for users. Period.  They only expose the controls necessary to write third
        party apps which act on behalf of users, only if authorized by that user.  The only thing we
        could do is simulate interacting with the LinkedIn search while masquerading as a
        real person with an account and scrape the results.

    .. note::
    
        Both Twitter and LinkedIn offer a *find my contacts* feature to find people by email
        address.  We might be able to find a way to programmatically do this.

        #. Create new gmail account
        #. Add all emails we think belong to the person via Google API
        #. Add new gmail to linked in profile via LinkedIn API
        #. Call *find my contacts* on LinkedIn
        #. Receive valid contacts
        #. Build profile URLS for each contact
        #. Scrape profiles

    .. _any API endpoint: https://dev.twitter.com/faq#26
    """
    def __init__(self):
        pass
