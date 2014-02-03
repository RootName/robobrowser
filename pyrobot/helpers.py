"""
Convenience methods for working with BeautifulSoup objects.
"""

import re
from bs4 import BeautifulSoup
from bs4.element import Tag

def match_text(text, tag):
    if isinstance(text, (str, unicode)):
        return text in tag.text
    if isinstance(text, re._pattern_type):
        return text.search(tag.text)

def find_all(soup, name=None, attrs=None, recursive=True, text=None,
              limit=None, **kwargs):
    """The `find` and `find_all` methods of `BeautifulSoup` don't handle the
    `text` parameter combined with other parameters. This is necessary for
    e.g. finding links containing a string or pattern. This method first
    searches by text content, and then by the standard BeautifulSoup arguments.

    """
    if text is None:
        return soup.find_all(
            name, attrs or {}, recursive, text, limit, **kwargs
        )
    tags = soup.find_all(
        name, attrs, recursive, **kwargs
    )
    rv = []
    for tag in tags:
        if match_text(text, tag):
            rv.append(tag)
        if limit is not None and len(rv) >= limit:
            break
    return rv

def find(soup, name=None, attrs=None, recursive=True, text=None, **kwargs):
    """Modified find method; see `find_all`, above.

    """
    tags = find_all(
        soup, name, attrs or {}, recursive, text, 1, **kwargs
    )
    if tags:
        return tags[0]

def ensure_soup(value):
    """Coerce a value (or list of values) to BeautifulSoup (or list of
    BeautifulSoups).

    :param value: String, BeautifulSoup, Tag, or list of the above
    :return: BeautifulSoup or list of BeautifulSoups

    """
    if isinstance(value, Tag):
        return value
    if isinstance(value, list):
        return [
            ensure_soup(item)
            for item in value
        ]
    return BeautifulSoup(value)

def lowercase_attr_names(tag):
    """Lower-case all attribute names of the provided BeautifulSoup tag.
    Note: this mutates the tag's attribute names and does not return a new
    tag.

    :param Tag: BeautifulSoup tag

    """
    # Use list comprehension instead of dict comprehension for 2.6 support
    tag.attrs = dict([
        (key.lower(), value)
        for key, value in tag.attrs.iteritems()
    ])