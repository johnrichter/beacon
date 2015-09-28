import dns.resolver

class EmailMiner(object):
    """
    An object to determine email address validity and similarity to an individual across a
    variety of popular public and private email services.

    According to :rfc:`5321` section 3.5, the ``VRFY`` command exists to verify if a username
    exists and **may** include the full name of the user.  These commands are commonly disabled
    on most services for security reasons (e.g. deter spammers), including authenticated sessions.

    .. code::

        rcpt to: <somereallylongemailaddressthatdoesntwork584@gmail.com>
        250 2.1.5 OK i199sm3826946qhc.44 - gsmtp
        vrfy <somereallylongemailaddressthatdoesntwork584@gmail.com>
        252 2.1.5 Send some mail, I'll try my best d10sm3853854qhc.36 - gsmtp

    """
    max_email_address_length = 254
    email_services = [
        'aol.com', 'atmail.com', 'fastmail.com', 'getanemailaddress.info', 'gmail.com', 'gmx.com',
        'gmx.net', 'gmx.us', 'hushmail.com', 'hushmail.me', 'hush.com', 'hush.ai', 'mac.hush.com',
        'icloud.com', 'me.com', 'lycos.com', 'mail.com', 'email.com', 'outlook.com', 'hotmail.com',
        'protonmail.com', 'rediffmail.com', 'runbox.com', 'yahoo.com', 'yahdex.com', 'zoho.com'
    ]

    def get_email_addresses_with_usernames(self, usernames):
        """
        Enumerate possible email addresses for ``usernames``

        :param usernames: A list of usernames
        :return: A list of email addresses
        """
        email_addresses = []
        for username in usernames:
            for service in self.email_services:
                if len(username) + len('@') + len(service) <= self.max_email_address_length:
                    email_addresses.append(username + '@' + service)

        return email_addresses

    def is_valid_email_domain(self, domain):
        try:
            records = dns.resolver.query(domain, 'MX')
        except dns.exception.DNSException as e:
            # The domain doesn't exist
            return False

        return len(records) > 0
