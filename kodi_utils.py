# -*- coding: utf-8 -*-

"""
Kodi utilities
"""

import os
import xbmc
import xbmcgui
import xbmcaddon

ADDON = xbmcaddon.Addon()
ADDON_ID = ADDON.getAddonInfo("id")
ADDON_NAME = ADDON.getAddonInfo("name")
ADDON_PATH = ADDON.getAddonInfo("path").decode('utf-8')
ADDON_ICON = ADDON.getAddonInfo("icon").decode('utf-8')
ADDON_PROFILE = ADDON.getAddonInfo("profile")
ADDON_VERSION = ADDON.getAddonInfo("version")
PATH_ADDONS = xbmc.translatePath("special://home/addons/")
PATH_TEMP = xbmc.translatePath("special://temp")
if not ADDON_PATH:
    ADDON_PATH = '..'

def notify(message, image=None):
    """ Creates a notification dialog
    Args:
        message (str): The message to show in the dialog
        image   (str): Path to an icon for this dialog
    """
    dialog = xbmcgui.Dialog()
    dialog.notification(ADDON_NAME, message, icon=image, sound=False)
    del dialog