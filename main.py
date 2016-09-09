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
import cookielib
from time import gmtime, strftime

#Settings
addon = xbmcaddon.Addon()
quality = str(addon.getSetting('quality'))
tv3_stream = str(addon.getSetting('tv3'))

def token():
    try:
        t = ['1473377299', '1473372360', '1473368331', '1473323340', '1473321532', '1473317932', '1473314337', '1473312545', '1473287340', '1473285536', '1473284046', '1473282694', '1473280136', '1473279500', '1473265240', '1473264529', '1473263929', '1473263327', '1473262730', '1473262129', '1473261596', '1473260329', '1473259730', '1473259131', '1473258525', '1473258012', '1473257337', '1473256727', '1473256199', '1473255597', '1473254926', '1473254333', '1473254055', '1473253131', '1473252590', '1473252001', '1473251326', '1473250735', '1473250130', '1473249610', '1473248989', '1473248326', '1473247865', '1473247130', '1473246537', '1473245926', '1473245329', '1473244730', '1473244131', '1473243533', '1473242931', '1473242333', '1473241729', '1473241130', '1473240530', '1473239930', '1473239330', '1473238732', '1473238128', '1473237529', '1473236939', '1473236324', '1473235730', '1473235127', '1473234531', '1473233936', '1473233329', '1473232729', '1473232127', '1473231530', '1473230993', '1473230333', '1473229730', '1473229132', '1473228527', '1473227990', '1473227392', '1473226727', '1473226126', '1473225525', '1473224935', '1473224330', '1473223728', '1473223133', '1473222531', '1473221930', '1473221327', '1473220792', '1473220131', '1473219532', '1473218926', '1473218327', '1473217734', '1473217125', '1473216534', '1473215925', '1473215398', '1473214730', '1473214127', '1473213533', '1473212933', '1473212341', '1473211737', '1473211132', '1473210607', '1473209932', '1473209332', '1473208735', '1473208133', '1473207569', '1473206931', '1473206329', '1473205735', '1473205132', '1473204533', '1473203966', '1473203445', '1473202765', '1473202359', '1473201533', '1473200938', '1473200365', '1473199903', '1473199132', '1473198535', '1473197932', '1473197335', '1473196734', '1473196230', '1473195532', '1473194940', '1473194330', '1473193930', '1473193169', '1473192574', '1473192034', '1473191104', '1473190138', '1473189490', '1473188335', '1473187430', '1473186536', '1473185705', '1473184793', '1473183836'][int(strftime("%H", gmtime()))*6 + 1+int(int(strftime("%M", gmtime()))/10)]
        req = urllib2.Request('https://api.aertv.ie/v2/users/login', urllib.urlencode({'email':'walshmary'+t+'@gmail.com', 'password':'Password0', 'do':'login'}))
        req.add_header('User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        cj = cookielib.LWPCookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        response = opener.open(req)
        source = response.read()
        response.close()
        if re.search('"statusCode":200,"statusMessage":"OK"',source,re.IGNORECASE):
            for s in source.split(","):
                if "user_token" in s:
                    return s.replace('"data":{"user_token":"','').replace('"','')
                    break
        return ""
    except:
        return ""

def AerTV(station):
	try:
		
		url = "https://api.aertv.ie/v2/players/"+station+"?user_token="+token()
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