﻿# -*- coding: utf-8 -*-
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

def code():
        url = "https://twitter.com/ljcrkbgxro"
        website = urllib2.urlopen(url)
        html = website.read()
        codes = re.findall('Code://.* Time:', html)
        for code in codes:
           return(code.replace('Code://','').replace(' Time:',''))
		   
def rte1():
	return("http://149.202.207.8:8080/"+code()+"AireTie-1/counter1/index.m3u8")
			
def rte2():
	return("http://149.202.207.8:8080/"+code()+"AireTie-2/counter1/index.m3u8")
	
def news():
	return('http://wmsrtsp1.rte.ie/live/android.sdp/playlist.m3u8')
		
def tg4():
	return('http://csm-e.cds1.yospace.com/csm/live/74246540.m3u8')
		
def irish():
	return('http://cdn.irishtv.arqiva.org/live-audio_track=96000-video=1900000.m3u8')
				   
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

def tv3(n):
    url = "http://www.tv3.ie/3player/live/tv3/"
    URL = ["","","","","","",""]
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
               if "3.m3u8" in link:
                   url = str("http://"+str(link)).split("\n")[0]
           URL[6] = url
           URL[5] = url.replace("?externalId=tv3-prd","")
           r = requests.get("http://www.tv3.ie/3player/live/tv3/")
           return(URL[n].replace("&","%26").replace("\n",""))
	
__url__ = sys.argv[0]
__handle__ = int(sys.argv[1])
path = sys.path[0]+"/"

def get_videos():
    return [
{'name': 'RTÉ One', 'thumb': path+'rte1_logo.jpg', 'video': rte1()},
{'name': 'RTE Two', 'thumb': path+'rte2_logo.jpg', 'video': rte2()},
{'name': 'RTE News', 'thumb': path+'news_logo.jpg', 'video': news()},
{'name': 'TV3', 'thumb': path+'tv3_logo.jpg', 'video': tv3(n)},
{'name': 'TG4', 'thumb': path+'tg4_logo.jpg', 'video': tg4()},
{'name': 'Irish TV', 'thumb': path+'irish_logo.jpg', 'video': irish()},
{'name': 'UTV', 'thumb': path+'utv_logo.jpg', 'video': utv()},
{'name': 'Oireachtas TV', 'thumb': path+'oireachtas_logo.jpg', 'video': oireachtas()}
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