# -*- coding: utf-8 -*-

"""
Remove blocked Partis IPs from Elementum
"""

# Allow imports from parent dir
import os, sys, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

import xbmcgui
from iplist import iplist
from kodi_utils import notify, ADDON_PATH, ADDON_NAME
import datetime

def remove_blocked_ips():
    eIplistPath = os.path.join(ADDON_PATH, '..', 'plugin.video.elementum', 'resources', 'misc', 'pack-iplist')
    if os.path.isfile(eIplistPath):
        dialog = xbmcgui.DialogProgress()
        line1 = "Checking for blocked Partis IPs"
        line2 = "It can take couple of minutes"
        dialog.create(ADDON_NAME, line1, line2)

        eIplist = iplist()

        PARTIS_DOMAINS = ["announce.partis.si", "announce.partis.net", "announce.partis.my", "announce.partis.rs"]
        partisIpv6s = []
        for domain in PARTIS_DOMAINS:
            try:
                ipv6 = eIplist.getIpv6FromDomain(domain)
                partisIpv6s.append(ipv6)
            except Exception:
                pass
        
        dialog.update(15, line1, line2, "Parsing current list ...")
        eRanges = eIplist.parseFromFile(eIplistPath)

        dialog.update(50, line1, line2, "Looking for Partis IPs in the list and removing them ...")
        found = False
        for ipv6 in partisIpv6s:
            foundRange, foundPos, eRanges = eIplist.findAndRemove(ipv6, eRanges)
            if foundRange:
                found = True

        if found:
            dialog.update(75, line1, line2, "Saving updated list ...")
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