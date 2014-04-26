#!/usr/bin/env python

import sys
sys.path.insert(0, 'libs')
from google.appengine.api import urlfetch
urlfetch.set_default_fetch_deadline(45)
from bs4 import BeautifulSoup

from constants import BASE_URL, INTERVAL_BETWEEN_REQUESTS

def get_soup(page=''):
    """
    Returns a bs4 object of the page requested
    """
    url = '%s/%s' % (BASE_URL, page)
    result = urlfetch.fetch(url, deadline=45)
    content = result.content
    return BeautifulSoup(content)


def get_item_soup(story_id):
    """
    Returns a bs4 object of the requested story
    """
    return get_soup(page='item?id=' + str(story_id))
