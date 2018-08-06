# -*- coding: utf-8 -*-

from Partis import Partis
from Partis.utils import notify, decorateTorrents, ADDON_PATH
from elementum.provider import register, get_setting, log
import sys, os

# Handle settings callbacks
if len(sys.argv) > 1:
    method = sys.argv[1]
    try:
        iplistPath = os.path.join(ADDON_PATH, '..', 'plugin.video.elementum', 'resources', 'misc', 'pack-iplist')
        if method == 'checkIpBlockingStatus':
            if os.path.isfile(iplistPath):
                notify('IP blocking is ENABLED within Elementum')
            else:
                notify('IP blocking is DISABLED within Elementum')
            sys.exit()
        elif method == 'disableIpBlocking':
            if os.path.isfile(iplistPath):
                os.rename(iplistPath, iplistPath+'.backup')
                notify('IP blocking is now DISABLED within Elementum')
            else:
                notify('IP blocking is already DISABLED within Elementum')
            sys.exit()
        elif method == 'enableIpBlocking':
            if os.path.isfile(iplistPath):
                notify('IP blocking is already ENABLED within Elementum')
            else:
                if os.path.isfile(iplistPath+'.backup'):
                    os.rename(iplistPath+'.backup', iplistPath)
                    notify('IP blocking is now ENABLED within Elementum')
                else:
                    notify('IP blocking cannot be enabled since the original list is no longer available')
            sys.exit()
    except Exception as e:
        log.debug(getattr(e, 'message', repr(e)))
        notify(getattr(e, 'message', repr(e)))
        pass


def do_search(query, category = None):
	try:
		partis = Partis(get_setting('username', unicode), get_setting('password', unicode))
		return decorateTorrents(partis.search(query, category))
	except Exception as e:
		log.debug(getattr(e, 'message', repr(e)))
		notify(getattr(e, 'message', repr(e)))
		return []

# Raw search
# query is always a string
def search(query):
	return do_search(query)

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
