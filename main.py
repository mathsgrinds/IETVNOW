# -*- coding: utf-8 -*-
# Module: default
# Author: MathsGrinds
# Created on: 03.04.2016
# License: GPL v.3 https://www.gnu.org/copyleft/gpl.html
# --------------------------------------------------------------------------------
# IMPORT
# --------------------------------------------------------------------------------
import os
import sys
import csv
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
import json
from urllib2 import urlopen
# --------------------------------------------------------------------------------
#Settings
# --------------------------------------------------------------------------------
addon = xbmcaddon.Addon()
username = str(addon.getSetting('email'))
password = str(addon.getSetting('password'))
__url__ = sys.argv[0]
__handle__ = int(sys.argv[1])
path = sys.path[0]+"/"
# --------------------------------------------------------------------------------
# SCRAPER
# --------------------------------------------------------------------------------
def Ustvnow(username, password):
    try:
        station = {"ABC":"", "CBS":"", "CW":"", "FOX":"", "NBC":"", "PBS":"", "My9":""}
        with requests.Session() as s:
            ### Get CSRF Token ###       
            url="https://watch.ustvnow.com/account/signin"
            r = s.get(url)
            html = r.text
            html = ' '.join(html.split())
            ultimate_regexp = "(?i)<\/?\w+((\s+\w+(\s*=\s*(?:\".*?\"|'.*?'|[^'\">\s]+))?)+\s*|\s*)\/?>"
            for match in re.finditer(ultimate_regexp, html):
                i = repr(match.group())
                if '<input type="hidden" name="csrf_ustvnow" value="' in i:
                    csrf = i.replace('<input type="hidden" name="csrf_ustvnow" value="','').replace('">','')
                    csrf = str(csrf).replace("u'","").replace("'","")
            ### Get Token ###
            url = "https://watch.ustvnow.com/account/login"
            payload = {'csrf_ustvnow': csrf, 'signin_email': username, 'signin_password':password, 'signin_remember':'1'}
            r = s.post(url, data=payload)
            html = r.text
            html = ' '.join(html.split())
            html = html[html.find('var token = "')+len('var token = "'):]
            html = html[:html.find(';')-1]
            token = str(html)
            ### Get Stream ###
            device = "gtv"        
            url = "http://m-api.ustvnow.com/"+device+"/1/live/login"
            payload = {'username': username, 'password': password, 'device':device}
            r = s.post(url, data=payload)
            html = r.text
            j = json.loads(html)
            result = j['result']
            url = "http://m-api.ustvnow.com/gtv/1/live/playingnow?token="+token
            r = s.get(url)
            html = r.text
            j = json.loads(html)
            n = 0
            while True:
                scode = j['results'][n]['scode']
                stream_code = j['results'][n]['stream_code']
                url = "http://m.ustvnow.com/stream/1/live/view?scode="+scode+"&token="+token+"&br_n=Firefox&br_v=54&br_d=desktop"
                r = s.get(url)
                html = r.text
                try:
                    i = json.loads(html)
                except:
                    break
                station[stream_code] = i["stream"]
                n += 1
            return station
    except:
        xbmc.executebuiltin('Notification(Login Failed, username and/or password is incorrect.)')
        return ""

# --------------------------------------------------------------------------------
# STREAMS
# --------------------------------------------------------------------------------
def streams():
    station = Ustvnow(username, password)
    return [{'name': "ABC", 'thumb': path+'resources/logos/ABC.png', 'link': station["ABC"]},
{'name': "CBS", 'thumb': path+'resources/logos/CBS.png', 'link': station["CBS"]},
{'name': "CW", 'thumb': path+'resources/logos/CW.png', 'link': station["CW"]},
{'name': "FOX", 'thumb': path+'resources/logos/FOX.png', 'link': station["FOX"]},
{'name': "NBC", 'thumb': path+'resources/logos/NBC.png', 'link': station["NBC"]},
{'name': "PBS", 'thumb': path+'resources/logos/PBS.png', 'link': station["PBS"]},
{'name': "My9", 'thumb': path+'resources/logos/My9.png', 'link': station["My9"]}]
# --------------------------------------------------------------------------------
# ROUTER
# --------------------------------------------------------------------------------
def router(paramstring):
    params = dict(parse_qsl(paramstring[1:]))
    if params:
        if params['mode'] == 'play':
            play_item = xbmcgui.ListItem(path=params['link'])
            xbmcplugin.setResolvedUrl(__handle__, True, listitem=play_item)
    else:
        for stream in streams():
            list_item = xbmcgui.ListItem(label=stream['name'], thumbnailImage=stream['thumb'])
            list_item.setProperty('fanart_image', stream['thumb'])
            list_item.setProperty('IsPlayable', 'true')
            url = '{0}?mode=play&link={1}'.format(__url__, stream['link'])
            xbmcplugin.addDirectoryItem(__handle__, url, list_item, isFolder=False)
        xbmcplugin.endOfDirectory(__handle__)
# --------------------------------------------------------------------------------
# MAIN
# --------------------------------------------------------------------------------
if __name__ == '__main__':
    router(sys.argv[2])
