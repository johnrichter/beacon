import birdy   # This Twitter API package can easily be slightly modified and used for AngelList


class AngelListMiner(object):
    """
    Retrieves information about an AngelList user.

    profile picture, and full name.  We may be able to parse the bio, what_i_do
    and what_ive_built, for email and username information.

    API Endpoints:
    * GET /users/search
        * *slug* - The URL slug of the desired user. i.e. https://angel.co/{slug}
        * *md5* - An MD5 hex hash of the email address of the desired user.

    Field Names (that we care about):
    * *aboutme_url* - A URL to the person's about.me profile
    * *behance_url* - A URL to the person's Behance.net profile
    * *blog_url* - A URL to the person's blog, possibly a personal website
    * *online_bio_url* - A URL to the person's online bio, possibly a personal website
    * *twitter_url* - A URL to the person's Twitter profile
    * *facebook_url* - A URL to the person's Facebook profile
    * *linkedin_url* - A URL to the person's LinkedIn profile
    * *angellist_url* - A URL to the person's AngelList profile (this is redundant)
    * *github_url* - A URL to the person's GitHub profile
    * *dribble_url* - A URL to the person's Dribble profile
    * *resume_url* - A URL to the person's resume.  May be a pdf, docx, website, etc
    * *image* - A URL to the person's profile picture
    * *name* - The person's full name, short name, or nickname
    * *what_i_do* - A blurb about the person's career, may contain email/username information
    * *what_ive_built* - A blurb abut the person's achievements, may contain email/username
      information
    """
    def __init__(self):
        pass
