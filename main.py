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

def tv3():
    url = "http://www.tv3.ie/3player/live/tv3/"
    website = urllib2.urlopen(url)
    html = website.read()
    uniques = re.findall('"(/3player/assets/css/global_v4\.css\?ver\=1\.2\&t\=.*?)"', html)
    for unique in uniques:
            u = unique.replace("/3player/assets/css/global_v4.css?ver=1.2&t=","")
    links = re.findall('"((http|ftp)s?://.*?)"', html)
    for link in links:
       if "m3u8" in link[0]:
           url = link[0]
           url = url+";externalId=tv3-prd&yo.ac=true&yo.sl=3&yo.po=5&yo.ls=1,2,3&unique="+u
           url = url.replace("&","%26")
           return(url)
	
__url__ = sys.argv[0]
__handle__ = int(sys.argv[1])
path = sys.path[0]+"/"

VIDEOS = {'Live Irish TV':[
{'name': 'RTÉ One', 'thumb': path+'rte1.jpg', 'video': rte1()},
{'name': 'RTE Two', 'thumb': path+'rte2.jpg', 'video': rte2()},
{'name': 'RTE News', 'thumb': path+'news.jpg', 'video': news()},
{'name': 'TV3', 'thumb': path+'tv3.jpg', 'video': tv3()},
{'name': 'TG4', 'thumb': path+'tg4.jpg', 'video': tg4()},
{'name': 'Irish TV', 'thumb': path+'irish.jpg', 'video': irish()},
{'name': 'UTV', 'thumb': path+'utv.jpg', 'video': utv()},
{'name': 'Oireachtas TV', 'thumb': path+'oireachtas.jpg', 'video': oireachtas()}
]}

def get_categories():
    return VIDEOS.keys()

def get_videos(category):
    return VIDEOS[category]

def list_categories():
    categories = get_categories()
    for category in categories:
        list_item = xbmcgui.ListItem(label=category, thumbnailImage=VIDEOS[category][0]['thumb'])
        list_item.setProperty('fanart_image', VIDEOS[category][0]['thumb'])
        url = '{0}?action=listing&category={1}'.format(__url__, category)
        xbmcplugin.addDirectoryItem(__handle__, url, list_item, isFolder=True)
    xbmcplugin.addSortMethod(__handle__, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    xbmcplugin.endOfDirectory(__handle__)

def list_videos(category):
    videos = get_videos(category)
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
            list_videos(params['category'])
        elif params['action'] == 'play':
            play_video(params['video'])
    else:
        list_categories()

if __name__ == '__main__':
    router(sys.argv[2])