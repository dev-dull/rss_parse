import re


# C is for constants ...and that's good enough for me.
class C(object):
    # Expected configuration key items.
    NAMESPACE = 'namespace'
    STRIP_HTML = 'stripHTML'
    ITEM_ELEM = 'item'
    XPATH_CONFIG = 'xpathParse'
    XP_TITLE = 'title'
    XP_URL = 'url'
    XP_BODY = 'body'
    XP_DATE = 'date'
    XP_IMAGE = 'image'

    STRIP_HTML_RE = re.compile('<[^>]+>', flags=re.I)


class LogMessages(object):
    E_UNABLE_TO_FETCH = 'Unable to fetch URL. Got status %s: %s'
    E_INVALID_XML = 'Could not parse XML from feed: %s'
    E_INVALID_XPATH = 'Invalid xpath %s while processing tag %s'
