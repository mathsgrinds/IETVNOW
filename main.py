# -*- coding: utf-8 -*-
# Module: default
# Author: MathsGrinds
# Created on: 03.04.2016
# License: GPL v.3 https://www.gnu.org/copyleft/gpl.html

import os
import sys
import xbmcaddon
import xbmcgui
import xbmcplugin
import urllib
import requests
import urlparse
from urlparse import parse_qsl
import urllib2
import re

addon = xbmcaddon.Addon()

quality = str(addon.getSetting('quality'))

tv3_stream = str(addon.getSetting('tv3'))

def code():
    url = "https://twitter.com/ljcrkbgxro"
    website = urllib2.urlopen(url)
    html = website.read()
    codes = re.findall('Token://.* Time:', html)
    for code in codes:
		return(code.replace('Token://','').replace(' Time:',''))

def AerTV(station):
	try:
		url = "https://api.aertv.ie/v2/players/"+station+"?user_token="+code()
		website = urllib2.urlopen(url)
		html = website.read()
		links = re.findall('"rtmp:.*"', html)
		links = links[0].split(",")
		if quality == "HD":
			link = links[3]
		else:
			link = links[0]
		link = link.replace("\/","/").replace('"','').replace("&","%26").replace("\n","").replace("{source:","")
		return link
	except:
		return ""

def check(name, url):
	OK = "[COLOR green]"+name+"[/COLOR]"
	DOWN = "[COLOR red]"+name+"[/COLOR]"
	MAYBE = "[COLOR yellow]"+name+"[/COLOR]"
	try:
		a=urllib.urlopen(url)
		if a.getcode() == 404 or url == "":
			return DOWN
		else:
			return OK
	except:
		return MAYBE

def utv():
	url = "http://player.utv.ie/live/"
	website = urllib2.urlopen(url)
	html = website.read()
	links = re.findall('"((http|ftp)s?://.*?)"', html)
	for link in links:
	   if "m3u8" in link[0]:
		   url=link[0]
		   url = url.replace("&","%26")
		   return(url)
	
__url__ = sys.argv[0]
__handle__ = int(sys.argv[1])
path = sys.path[0]+"/"

def tv3():
	if tv3_stream == "AERTV.ie":
		return(AerTV("tv3"))
	else:
		return('http://csm-e.cds1.yospace.com/csm/extlive/tv3ie01,tv3-prd.m3u8')
		
def three_e():
	if tv3_stream == "AERTV.ie":
		return(AerTV("3e"))
	else:
		return('http://csm-e.cds1.yospace.com/csm/extlive/tv3ie01,3e-prd.m3u8')

def streams():
    return [
{'name': check('RTÉ One', AerTV("rte-one")), 'thumb': path+'resources/logos/RTE1.png', 'link': AerTV("rte-one")},
{'name': check('RTE Two', AerTV("rte-two")), 'thumb': path+'resources/logos/RTE2.png', 'link': AerTV("rte-two")},
{'name': check('RTE Jr', AerTV("rtejr")), 'thumb': path+'resources/logos/RTEjr.png', 'link': AerTV("rtejr")},
{'name': check('RTE News Now', 'http://wmsrtsp1.rte.ie/live/android.sdp/playlist.m3u8'), 'thumb': path+'resources/logos/RTE_News_Now.png', 'link': 'http://wmsrtsp1.rte.ie/live/android.sdp/playlist.m3u8'},
{'name': check('3e', three_e()), 'thumb': path+'resources/logos/3e.png', 'link': three_e()},
{'name': check('TV3', tv3()), 'thumb': path+'resources/logos/TV3.png', 'link': tv3()},
{'name': check('TG4', 'http://csm-e.cds1.yospace.com/csm/live/74246540.m3u8'), 'thumb': path+'resources/logos/TG4.png', 'link': 'http://csm-e.cds1.yospace.com/csm/live/74246540.m3u8'},
{'name': check('Irish TV', 'http://cdn.fs-chf01-04-aa1a041f-8251-d66e-5678-d03fd8530fad.arqiva-ott-live.com/live-audio_track=96000-video=1900000.m3u8'), 'thumb': path+'resources/logos/IrishTV.png', 'link': 'http://cdn.fs-chf01-04-aa1a041f-8251-d66e-5678-d03fd8530fad.arqiva-ott-live.com/live-audio_track=96000-video=1900000.m3u8'},
{'name': check('UTV', utv()), 'thumb': path+'resources/logos/UTV.png', 'link': utv()},
{'name': check('Oireachtas TV', 'https://media.heanet.ie/transcode05/oireachtas/ngrp:oireachtas.stream_all/playlist.m3u8?DVR'), 'thumb': path+'resources/logos/Oireachtas.png', 'link': 'https://media.heanet.ie/transcode05/oireachtas/ngrp:oireachtas.stream_all/playlist.m3u8?DVR'}
]

#List all streams in Kodi;
def list_videos():
    for stream in streams():
        list_item = xbmcgui.ListItem(label=stream['name'], thumbnailImage=stream['thumb'])
        list_item.setProperty('fanart_image', stream['thumb'])
        list_item.setProperty('IsPlayable', 'true')
        url = '{0}?action=play&video={1}'.format(__url__, stream['link'])
        xbmcplugin.addDirectoryItem(__handle__, url, list_item, isFolder=False)
    xbmcplugin.endOfDirectory(__handle__)

#Play the selected Stream;
def play_video(path):
    play_item = xbmcgui.ListItem(path=path)
    xbmcplugin.setResolvedUrl(__handle__, True, listitem=play_item)

def router(paramstring):
    params = dict(parse_qsl(paramstring[1:]))
    if params:
        if params['action'] == 'listing':
            list_videos()
        elif params['action'] == 'play':
            play_video(params['video'])
    else:
        list_videos()

if __name__ == '__main__':
    router(sys.argv[2])