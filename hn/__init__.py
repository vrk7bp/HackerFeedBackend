"""
Python API for Hacker News.

@author Karan Goel
@email karan@goel.im
"""
from .DBBackend.version import VERSION

__title__ = 'hackernews'
__version__ = VERSION
__author__ = 'Karan Goel'
__license__ = 'MIT'
__copyright__ = 'Copyright 2014 Karan Goel'

from .DBBackend.hn import HN, Story
