import arrow
import logging
import requests
from lxml import etree
from dateutil import parser
from .rss_parse_consts import C, LogMessages


class RSSParser(list):
    def __init__(self, url, xpath_config):
        result = None
        # TODO: news_feed.__init__: handle authenticated proxy nonsense.
        try:
            result = requests.get(url)
            if result.status_code == 200:
                root = etree.fromstring(result.content)
            else:
                # if we didn't get a solid result, treat it the same as an error.
                # TODO: news_feed.__init__: see if requests.get() handles redirects for us.
                raise requests.exceptions.ConnectionError
        except requests.exceptions.ConnectionError as e:
            logging.error(LogMessages.E_UNABLE_TO_FETCH % (result.status_code if result else '<timeout>', url))
        except etree.XMLSyntaxError as e:
            logging.error(LogMessages.E_INVALID_XML % url)
        else:
            # effectively skip doing anything if we couldn't get or parse the feed.
            # TODO: news_feed.__init__: I'm unsure how the rest of the app will behave to an empty (subclassed) list.
            for e in root.xpath(xpath_config[C.XPATH_CONFIG][C.ITEM_ELEM]):
                # REMINDER! You overrode the append method.
                self.append(*self._parse(e, xpath_config[C.XPATH_CONFIG]))

    def _parse(self, e, xpath_config):
        url = (self._safe_xpath(e, xpath_config[C.XP_URL], xpath_config[C.NAMESPACE]) or b'').decode()
        title = (self._safe_xpath(e, xpath_config[C.XP_TITLE], xpath_config[C.NAMESPACE]) or b'').decode()
        body = (self._safe_xpath(e, xpath_config[C.XP_BODY], xpath_config[C.NAMESPACE]) or b'').decode()
        date = (self._safe_xpath(e, xpath_config[C.XP_DATE], xpath_config[C.NAMESPACE]) or b'').decode()
        image = (self._safe_xpath(e, xpath_config[C.XP_IMAGE], xpath_config[C.NAMESPACE]) or b'').decode()

        body = C.STRIP_HTML_RE.sub('', body) if xpath_config[C.STRIP_HTML] else body
        return url, title, body, parser.parse(date), image

    @staticmethod
    def _safe_xpath(e, xp, ns):
        try:
            item = e.xpath(xp, namespaces=ns)
        except etree.XPathEvalError:
            logging.error(LogMessages.E_INVALID_XPATH%(xp, e.tag))
            return None

        # TODO: news_feed._safe_xpath: detect and transform text encoding instead of throwing stuff out.
        return item[0].encode('ascii', 'ignore') if item else None

    # override the append function to abstract away the init of _Story
    def append(self, url, title, body, date, image=None):
        return super().append(self._Story(url, title, body, date, image))

    # nested class
    class _Story(object):
        def __init__(self, url, title, body, date, image):
            self.url = url
            self.title = title
            self.body = body
            # TODO: _story.__init__: arrow.get and dateutil.parser.parse probably throw errors that need handled.
            self.date = arrow.get(date)
            self.image = image if not image or image.lower().startswith('http') else 'http://'+image
