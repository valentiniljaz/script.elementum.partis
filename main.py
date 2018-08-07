# -*- coding: utf-8 -*-

from Partis import Partis
from kodi_utils import notify, ADDON_PATH, ADDON_NAME
from elementum.provider import register, get_setting, log
from iplist import iplist
import sys, os, datetime
import xbmcgui

# Handles settings callbacks
if len(sys.argv) > 1:
    method = sys.argv[1]
    try:
        eIplistPath = os.path.join(ADDON_PATH, '..', 'plugin.video.elementum', 'resources', 'misc', 'pack-iplist')
        if method == 'removeBlockedIps':
            if os.path.isfile(eIplistPath):
                dialog = xbmcgui.DialogProgress()
                line1 = "Checking for blocked Partis IPs"
                dialog.create(ADDON_NAME, line1)

                eIplist = iplist()

                PARTIS_DOMAINS = ["announce.partis.si", "announce.partis.net", "announce.partis.my", "announce.partis.rs"]
                partisIpv6s = []
                for domain in PARTIS_DOMAINS:
                    try:
                        ipv6 = eIplist.getIpv6FromDomain(domain)
                        partisIpv6s.append(ipv6)
                    except Exception:
                        pass
                
                dialog.update(15, line1, "Parsing current list ...")
                eRanges = eIplist.parseFromFile(eIplistPath)

                dialog.update(50, line1, "Looking for Partis IPs in the list ...")
                found = False
                for ipv6 in partisIpv6s:
                    foundRange, foundPos, eRanges = eIplist.findAndRemove(ipv6, eRanges)
                    if foundRange:
                        found = True

                if found:
                    dialog.update(70, line1, "Writing updated list ...")
                    now = str(datetime.datetime.now())
                    now = now.replace(" ", "--")
                    now = now.replace(":", "-")
                    now = now.replace(".", "-")
                    os.rename(eIplistPath, eIplistPath + '.backup_' + now)
                    eIplist.writeToFile(eIplistPath, eRanges)
                    dialog.close()
                    del dialog
                    notify("Partis IPs were removed from blocked list in Elementum. Restart KODI!")
                else:
                    dialog.close()
                    del dialog
                    notify("IP blocking is ENABLED but Partis IPs are not blocked. You\'re good!")
            else:
                notify("IP blocking is DISABLED within Elementum. You\'re good!")
            sys.exit()
    except Exception as e:
        log.debug(getattr(e, 'message', repr(e)))
        notify(getattr(e, 'message', repr(e)))
        pass

# Handles searches by Elementum
def do_search(query, category = None):
    try:
        partis = Partis(get_setting('username', unicode), get_setting('password', unicode))
        return partis.updateIconPath(partis.search(query, category), os.path.join(ADDON_PATH, 'Partis'))
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
