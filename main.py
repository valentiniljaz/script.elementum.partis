# -*- coding: utf-8 -*-

from Partis import Partis
from helpers.kodi_utils import notify, notice, ADDON_PATH
from elementum.provider import register, get_setting, log
from helpers.remove_blocked_ips import remove_blocked_ips
import sys, os

# Handles settings callbacks
if len(sys.argv) > 1:
    method = sys.argv[1]
    try:
        if method == 'removeBlockedIps':
            remove_blocked_ips()
            sys.exit()
    except Exception as e:
        log.debug(getattr(e, 'message', repr(e)))
        notify(getattr(e, 'message', repr(e)))
        pass

# Handles searches by Elementum
def do_search(query, category = None):
    notice('Search query: ' + str(query))
    try:
        partis = Partis(get_setting('username', unicode), get_setting('password', unicode))
        notify('Searching ...')
        return partis.updateIconPath(partis.search(query, category), os.path.join(ADDON_PATH, 'Partis'))
    except Exception as e:
        log.debug(getattr(e, 'message', repr(e)))
        notify(getattr(e, 'message', repr(e)))
        return []

# Raw search
# {
#    "query": "rampage",
#    "proxy_url"; ""
# }
def search(query):
    return do_search("%(query)s" % query)

# Movie Payload Sample
# Note that "titles" keys are countries, not languages
# The titles are also normalized (accents removed, lower case etc...)
# {
#     "imdb_id": "tt1254207",
#     "title": "big buck bunny",
#     "year": 2008,
#     "titles": {
#         "es": "el gran conejo",
#         "nl": "peach open movie project",
#         "ru": "большои кролик",
#         "us": "big buck bunny short 2008"
#     }
# }
def search_movie(movie):
    return do_search("%(title)s %(year)d" % movie, 'movies')


# Episode Payload Sample
# {
#     "imdb_id": "tt0092400",
#     "tvdb_id": "76385",
#     "title": "married with children",
#     "season": 1,
#     "episode": 1,
#     "titles": null
# }
def search_episode(episode):
    return do_search("%(title)s S%(season)02dE%(episode)02d" % episode, 'series')


# Episode Payload Sample
# {
#     "imdb_id": "tt0092400",
#     "tvdb_id": "76385",
#     "title": "married with children",
#     "season": 1,
#     "titles": null
# }
def search_season(season):
    return do_search("%(title)s Season %(season)d" % season, 'series')


# Register module for use
register(search, search_movie, search_episode, search_season)
