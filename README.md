# rss_parse
## About rss_parse:
rss_parse is a module for Python 3.4.2 or newer. It takes an RSS feed URL and a dictionary object that contains xpaths to the relevent data as input, fetchs the RSS feed data, parses it, and returns it as an iterable object where each element contains the following details from each `<item>` in the RSS feed: title, body, url, publication date, and image resource URL.

## Sample Usage:
### Using a standard Python dictionary as a configuration object.
```
from rss_parse import RSSParser

rss_url = 'http://www.jpl.nasa.gov/multimedia/rss/news.xml'
xpath_configuration = { 'xpathParse': { 
                  'stripHTML': True,
                  'item': '/rss/channel/item',
                  'namespace': {'re': 'http://exslt.org/regular-expressions'},
                  'title': './/title/text()',
                  'url': './/link/text()',
                  'body': './/description/text()',
                  'date': './/pubDate/text()',
                  'image': '((re:match(.//description/text(), '
                           '\'www.jpl.nasa.gov/images/[^\\">]+\', '
                           "'g')/text()) | /rss/channel/image/url/text())[1]"
                  }}

parsed_feed = RSSParser(rss_url, xpath_configuration)
print(parsed_feed[0].title)
```

rss_parse.RSSParser uses XPaths to identify the various parts of a news article in an RSS feed. XPaths are an entire separate topic not covered in this documentation. However, you can generally think of them as being like a directory structure where the first item in the path encapsulates the subsequent items. So given the XML <foo><bar><baz1></baz1><baz2>Hi!</baz2></bar></foo>, the XPath /foo/bar/baz2 would point us at the data in the baz2 item and /foo/bar/baz2/text() would give us just the text Hi!
> **NOTE:** Except for the XPath for the `item` key, all XPaths are relative to the `<item>` tag.


####In top-down ordering, we see the following:
#### Key: `xpathParse:`
  Value: The value is a dictionary containing the following key:value pairs.

#### Key: `stripHTML:`
  Value: This will either be `true` or `false` depending on if the RSS feed has undesired HTML content in the main body (description/summary) text. Generally it's a good idea to simply set this to `true`. However, some RSS feeds, such as Google News, add links to recommended stories. Stripping HTML in those cases can make the summary text confusing to read. A future version of xkcd_news will have an additional option to fine-tune what content should be stripped from the feed. A future version of rss_parse will permit this value to be a regular expression that represents what html should be removed, and what should be kept.

#### Key: `item:` 
  Value: This is a fully specified XPath to news items (headlines/articles) in the feed. Generally, this will never need to be changed. The exception might be for Atom feeds wich use a slightly different specification that is similar to RSS.

#### Key: `namespace:` 
 Value: Namespaces are a part of XML and deserve their own section that won't be covered here. In xkcd_news, they're generally used to help specify the XPath to an image associated with a specific news item in the RSS feed. In the example, we'll add a namespace so we can specify a non-standard RSS tag in a format specification provided by Yahoo.

#### Key: `title:`
  Value: This value is a relative XPath where the specific item in the XPath `/rss/channel/item` is handled for you. This is the effectively the headline of the news article. It is unlikely you will need to change this.

#### Key: `url:`
  Value: This is the relative XPath that specifies a link to the full news article. It is unlikely you will need to change this.

#### Key: `body:`
  Value: This is the relative XPath that specifies the summary/description text of the news article. It is unlikely you will need to change this.

#### Key: `date:`
  Value: This is the relative XPath that specifies the publication date of the news article. It is unlikely you will need to change this. This date value determines the order of the final output. 

#### Key: `image:`
  Value: An image is not part of the default RSS specification. The result is that this value will likely need to be changed for every RSS feed added to `feeds.yaml`. The default `feeds.yaml` configuration comes with examples on how to find an image resource in the article summary/body by regular expressions (see uses of the 're' namespace), by non-standard tags (see uses of the 'yahoo' namespace), by simply defaulting to the main image of the feed (see the above starting sample), and by using an XPath that gives us the image URL via regular expression if one is available, otherwise defaulting to the main feed image (effectively mixing two of the previous options).

#### The RSSParser() Output:
The output from creating the RSSParser can be treated as a list. Each item in that list contains the values retreived by the associated XPaths (as described above). To build on the above example, we could do the following with the parsed_feed variable.

```
for item in parsed_feed:
  print(item.url) # the URL to the specific <item> in the RSS feed. (e.g. a link to a news story)
  print(item.title) # the title of the <item> (e.g. the headline of a news article)
  print(item.body) # the main body text of the <item> (e.g. the summary text of a news article)
  print(item.date) # the date the <item> was added or updated in the RSS feed (e.g. the publication date of a news article)
  print(item.image) # the URL to an image associated with <item>. This is sometimes None. (e.g. the logo of a news service)
```

### Other Configuration formats:
> *NOTE:* You must convert these into a Python dictionary before passing them to RSSParser(). The below is for formatting reference.
#### YAML:
```
xpathParse:
  stripHTML: true
  item: '/rss/channel/item'
  namespace: 
    re: http://exslt.org/regular-expressions
  title: .//title/text()
  url: .//link/text()
  body: .//description/text()
  date: .//pubDate/text()
  image: ((re:match(.//description/text(), 'www.jpl.nasa.gov/images/[^\">]+', 'g')/text()) | /rss/channel/image/url/text())[1]
```

#### JSON:
```
{
  "xpathParse": {
    "item": "/rss/channel/item",
    "url": ".//link/text()",
    "body": ".//description/text()",
    "date": ".//pubDate/text()",
    "stripHTML": true,
    "namespace": {
      "re": "http://exslt.org/regular-expressions"
    },
    "title": ".//title/text()",
    "image": "((re:match(.//description/text(), 'www.jpl.nasa.gov/images/[^\\\">]+', 'g')/text()) | /rss/channel/image/url/text())[1]"
  }
}
```
