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

n = int(addon.getSetting('tv3.stream.number'))
quality = str(addon.getSetting('quality'))

def code():
    url = "https://twitter.com/ljcrkbgxro"
    website = urllib2.urlopen(url)
    html = website.read()
    codes = re.findall('Token://.* Time:', html)
    for code in codes:
		return(code.replace('Token://','').replace(' Time:',''))

def stream(station):
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

def rte1():
	return stream("rte-one")

def rte2():
	return stream("rte-two")

def rtejr():
	return stream("rtejr")

def threeE():
	return stream("3e")
	
def news():
	return('http://wmsrtsp1.rte.ie/live/android.sdp/playlist.m3u8')
		
def tg4():
	return('http://csm-e.cds1.yospace.com/csm/live/74246540.m3u8')
		
def irish():
	return('http://cdn.fs-chf01-04-aa1a041f-8251-d66e-5678-d03fd8530fad.arqiva-ott-live.com/live-audio_track=96000-video=1900000.m3u8')
				   
def oireachtas():
	return('https://media.heanet.ie/transcode05/oireachtas/ngrp:oireachtas.stream_all/playlist.m3u8?DVR')

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

def tv3():
    url = "http://www.tv3.ie/3player/live/tv3/"
    URL = ["","","","","","","","",""]
    website = urllib2.urlopen(url)
    html = website.read()
    uniques = re.findall('"(/3player/assets/css/global_v4\.css\?ver\=1\.2\&t\=.*?)"', html)
    for unique in uniques:
            u = unique.replace("/3player/assets/css/global_v4.css?ver=1.2&t=","")
    links = re.findall('"((http|ftp)s?://.*?)"', html)
    for link in links:
       if "m3u8" in link[0]:
			url = link[0]
			url = str(url)
			URL[2] = url
			url = url[:url.index('.m3u8')+len('.m3u8')]
			URL[1] = url
			url = url+";jsessionid=0&externalId=tv3-prd&yo.ac=true&yo.sl=3&yo.po=5&yo.ls=1,2,3&unique="+u
			URL[4] = url
			URL[3] = url.replace(";jsessionid=0&","?")
			response = requests.session().get(url)
			for link in response.text.split("http://"):
				if quality == "HD":
					if "4.m3u8" in link:
						url = str("http://"+str(link)).split("\n")[0]
				else:
					if "2.m3u8" in link:
						url = str("http://"+str(link)).split("\n")[0]
			URL[6] = url
			URL[5] = url.replace("?externalId=tv3-prd","")
			r = requests.get("http://www.tv3.ie/3player/live/tv3/")
			URL[0] = stream("tv3")
			return(URL[n].replace("&","%26").replace("\n",""))
	
__url__ = sys.argv[0]
__handle__ = int(sys.argv[1])
path = sys.path[0]+"/"

def get_videos():
    return [
{'name': check('RTÉ One', rte1()), 'thumb': path+'rte1_logo.jpg', 'video': rte1()},
{'name': check('RTE Two', rte2()), 'thumb': path+'rte2_logo.jpg', 'video': rte2()},
{'name': check('RTE Jr', rtejr()), 'thumb': path+'rtejr_logo.jpg', 'video': rtejr()},
{'name': check('RTE News', news()), 'thumb': path+'news_logo.jpg', 'video': news()},
{'name': check('3e', threeE()), 'thumb': path+'3e_logo.jpg', 'video': threeE()},
{'name': check('TV3', tv3()), 'thumb': path+'tv3_logo.jpg', 'video': tv3()},
{'name': check('TG4', tg4()), 'thumb': path+'tg4_logo.jpg', 'video': tg4()},
{'name': check('Irish TV', irish()), 'thumb': path+'irish_logo.jpg', 'video': irish()},
{'name': check('UTV', utv()), 'thumb': path+'utv_logo.jpg', 'video': utv()},
{'name': check('Oireachtas TV', oireachtas()), 'thumb': path+'oireachtas_logo.jpg', 'video': oireachtas()}
]

def list_videos():
    videos = get_videos()
    for video in videos:
        list_item = xbmcgui.ListItem(label=video['name'], thumbnailImage=video['thumb'])
        list_item.setProperty('fanart_image', video['thumb'])
        list_item.setProperty('IsPlayable', 'true')
        url = '{0}?action=play&video={1}'.format(__url__, video['video'])
        xbmcplugin.addDirectoryItem(__handle__, url, list_item, isFolder=False)
    xbmcplugin.endOfDirectory(__handle__)

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