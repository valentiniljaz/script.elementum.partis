# Partis.si provider for Elementum

Add-on scrapes www.partis.si for torrent links and feeds them into [Elementum](https://github.com/elgatito/plugin.video.elementum).

## Installation

* install [Elementum](https://github.com/elgatito/plugin.video.elementum) on your Kodi
* enable unknown sources within your Kodi installation
* [download ZIP](https://github.com/valentiniljaz/script.elementum.partis/archive/master.zip) from this repo
* use "Install from zip" within Add-ons section of Kodi

## IP blocking

Elementum uses a list of IPs which are blocked from accessing by any method within Elementum. Among those IPs are also IPs of Partis announce servers.
Addon provides mechanism to remove those IPs from the list so that streaming can work for any Partis torrent.

Go to addon Config panel and then "IP blocking" >> "Remove blocked Partis IPs from Elementum". It will parse the existing list, remove any found Partis 
IPs and save back the list. After the operation you need to restart your Kodi for the list to take effect.

## Links

https://github.com/scakemyer/script.quasar.dummy

https://github.com/elgatito/script.elementum.burst

https://github.com/elgatito/plugin.video.elementum

https://github.com/anacrolix/torrent

## Disclaimer

The author does not host or distribute any of the content displayed by this addon. The author does not have any affiliation with the content providers.