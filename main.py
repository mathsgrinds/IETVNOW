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
import json
from urllib2 import urlopen

def str2bool(v):
   return v.lower() in ("yes", "true", "t", "1")

#Settings
addon = xbmcaddon.Addon()
quality = str(addon.getSetting('quality'))
Guide = str2bool(addon.getSetting('guide'))
RTENewsNowPreferredStream = str(addon.getSetting('RTENewsNowpreferredstream'))
TG4PreferredStream = str(addon.getSetting('TG4preferredstream'))
TV3PreferredStream = str(addon.getSetting('TV3preferredstream'))
ThreeEPreferredStream = str(addon.getSetting('ThreeEpreferredstream'))
UTVPreferredStream = str(addon.getSetting('UTVpreferredstream'))
email = str(addon.getSetting('email'))
password = str(addon.getSetting('password'))

useragent = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0'}

__url__ = sys.argv[0]
__handle__ = int(sys.argv[1])
path = sys.path[0]+"/"

def login():
    try:
    
        #Pre-Defined Accounts;
        t = ['1473377299', '1473372360', '1473368331', '1473323340', '1473321532', '1473317932', '1473314337', '1473312545', '1473287340', '1473285536', '1473284046', '1473282694', '1473280136', '1473279500', '1473265240', '1473264529', '1473263929', '1473263327', '1473262730', '1473262129', '1473261596', '1473260329', '1473259730', '1473259131', '1473258525', '1473258012', '1473257337', '1473256727', '1473256199', '1473255597', '1473254926', '1473254333', '1473254055', '1473253131', '1473252590', '1473252001', '1473251326', '1473250735', '1473250130', '1473249610', '1473248989', '1473248326', '1473247865', '1473247130', '1473246537', '1473245926', '1473245329', '1473244730', '1473244131', '1473243533', '1473242931', '1473242333', '1473241729', '1473241130', '1473240530', '1473239930', '1473239330', '1473238732', '1473238128', '1473237529', '1473236939', '1473236324', '1473235730', '1473235127', '1473234531', '1473233936', '1473233329', '1473232729', '1473232127', '1473231530', '1473230993', '1473230333', '1473229730', '1473229132', '1473228527', '1473227990', '1473227392', '1473226727', '1473226126', '1473225525', '1473224935', '1473224330', '1473223728', '1473223133', '1473222531', '1473221930', '1473221327', '1473220792', '1473220131', '1473219532', '1473218926', '1473218327', '1473217734', '1473217125', '1473216534', '1473215925', '1473215398', '1473214730', '1473214127', '1473213533', '1473212933', '1473212341', '1473211737', '1473211132', '1473210607', '1473209932', '1473209332', '1473208735', '1473208133', '1473207569', '1473206931', '1473206329', '1473205735', '1473205132', '1473204533', '1473203966', '1473203445', '1473202765', '1473202359', '1473201533', '1473200938', '1473200365', '1473199903', '1473199132', '1473198535', '1473197932', '1473197335', '1473196734', '1473196230', '1473195532', '1473194940', '1473194330', '1473193930', '1473193169', '1473192574', '1473192034', '1473191104', '1473190138', '1473189490', '1473188335', '1473187430', '1473186536', '1473185705', '1473184793', '1473183836'][int(strftime("%H", gmtime()))*6 + 1+int(int(strftime("%M", gmtime()))/10)]
        
        #If there isn't both Email and Password set;
        if not email and not password:
        
            #Use a Pre-Defined Free Account;
            req = urllib2.Request('http://api.aertv.ie/v2/users/login', urllib.urlencode({'email':'walshmary'+t+'@gmail.com', 'password':'Password0'}), useragent)
            
        else:
        
            #Use the Account defined in Settings by the User;
            req = urllib2.Request('https://api.aertv.ie/v2/users/login', urllib.urlencode({'email':email, 'password':password}), useragent)
            
        #Output the JSON;
        html = urllib2.urlopen(req).read()
        return json.loads(html)
        
    except:
    
        #Notify the user that the Email and Password is incorrect;
        xbmc.executebuiltin('Notification(Login Failed, The Email and/or Password is incorrect.)')
        return ""

#Login;
loginj = login()

def AerTV(channel):
    
    #Get the JSON from the Players API;
    req = urllib2.Request("https://api.aertv.ie/v2/players/"+channel+"?user_token="+loginj[u'data'][u'user_token'], None, useragent)
    html = urllib2.urlopen(req).read()
    j = json.loads(html)
    SD = ""
    HD = ""
    
    #For Each RTMP Stream;
    for item in j[u'data'][u'urls'][u'stream'][u'rtmp']:
    
        #If its bitrate is Greater Than or Equal to 500000 and less than 1500000;
        if int(item[u"bitrate"]) >= 500000 and int(item[u"bitrate"]) < 1500000:
            SD = item[u"source"] #Set the Streams Link to SD Variable;
            
        #If its bitrate is Greater Than or Equal to 1500000;
        if int(item[u"bitrate"]) >= 1500000:
            HD = item[u"source"] #Set the Streams Link to HD Variable;
            
        #If the HD Variable has no Stream Link (e.x RTEjr);
        if not HD:
            HD = SD #Set the HD Variable's link to the SD Link;
            
    #Return Stream based on the Quality Setting;
    if quality == "SD":
        return SD
    else:
        return HD
        
def guide(channel):
    
    #If the Guide is Enabled;
    if Guide:
        
        #Parse the show directly for certain channels;
        if channel=="RTE News Now":
            req = urllib2.Request('http://www.rte.ie/player/99/live/7/', None, useragent)
            html = urllib2.urlopen(req).read()
            return " - " + re.findall('<h1 id=\"show-title\">.*</h1>', html)[0].replace('<h1 id="show-title">','').replace('</h1>','').replace("&amp;", "and").replace(" & "," and ").replace('and#39;', ' ').replace('&Aacute;', 'A').replace('&Eacute;', 'E').replace('&Iacute;', 'I').replace('&Oacute;', 'O').replace('&Uacute;', 'U').replace('&aacute;', 'a').replace('&eacute;', 'e').replace('&iacute;', 'i').replace('&oacute;', 'o').replace('&uacute;', 'u').replace('&#39;', ' ')
        elif channel=="Irish TV":
            return " - Local Stories" #also breaks out of def;
        elif channel=="Oireachtas TV":
            return " - Parliamentary Television" #also breaks out of def;
        elif channel=="RTE One +1":
            return " - RTE One 1 hour ago"
        
        #Parse the urls for the Entertainment.ie channels;
        elif channel=="RTE One":
            url='http://entertainment.ie/tv/display.asp?channelid=81'
        elif channel=="RTE Two":
            url='http://entertainment.ie/tv/display.asp?channelid=82'
        elif channel=="RTEjr":
            url='http://entertainment.ie/tv/display.asp?channelid=1649'
        elif channel=="TV3":
            url='http://entertainment.ie/tv/display.asp?channelid=84'
        elif channel=="tg4":
            url='http://entertainment.ie/tv/display.asp?channelid=83'
        elif channel=="3e":
            url='http://entertainment.ie/tv/display.asp?channelid=1209'
        elif channel=="UTV":
            url='http://entertainment.ie/tv/display.asp?channelid=39'
        
        #Parse the show for the Entertainment.ie links;
        req = urllib2.Request(url, None, useragent)
        html = urllib2.urlopen(req).read()
        try:
            return " - " + re.findall('title=\".*\" onclick', html)[0].replace('title="','').replace('" onclick','').replace('View ','').replace(' programme details','').replace("&amp;", "and").replace(" & "," and ").replace('and#39;', ' ').replace('&Aacute;', 'A').replace('&Eacute;', 'E').replace('&Iacute;', 'I').replace('&Oacute;', 'O').replace('&Uacute;', 'U').replace('&aacute;', 'a').replace('&eacute;', 'e').replace('&iacute;', 'i').replace('&oacute;', 'o').replace('&uacute;', 'u')
        except:
            return " - Close"
    else:
        return ""
        
def parse(channel):

    #Get the Country;
    req = urllib2.Request('http://whatismycountry.com/', None, useragent)
    html = urllib2.urlopen(req).read()
    country = str(html)
    
    #If the user is not in Ireland and Channel is RTE One, Two or jr; or; If the user is not in Ireland or United Kingdom and Channel is Oireachtas TV;
    if ("Ireland" not in country and (channel == "RTE One" or channel == "RTE One +1" or channel == "RTE Two" or channel == "RTEjr")) or ("Ireland" not in country and "United Kingdom" not in country and channel == "Oireachtas TV"):
        
        #Change the Channels Name to Red and append "(Geo-Blocked!)"
        return "[COLOR red]"+channel+" (Geo-Blocked!)[/COLOR]"
        
    else:
        
        #Return the Channel Name with the Guide Data Appended;
        return channel + guide(channel)

#---------------------------------------------------------------------------------
# Channel Parsers

def scrape_m3u8(x, index=0, x_is_url = True):
    if x_is_url:
        req = urllib2.Request(x, None, useragent)
        html = urllib2.urlopen(req).read()
    else:
        html = x
    try:
        link = re.findall('\"https?\:\/\/.*\.m3u8.*?\"', html)[index]
    except:
        try:
            link = re.findall('\'https?\:\/\/.*\.m3u8.*?\'', html)[index]
        except:
            try:
                link = re.findall('https?\:\/\/.*\.m3u8.* ?', html)[index]
            except:
                link = ""
    return str(link).replace("&","%26").replace('"','').replace("'",'').replace(' ','')

def TG4():
	try:
		if TG4PreferredStream == "AerTV.ie":
			return AerTV("tg4")
		elif TG4PreferredStream == "TG4.ie":
			return scrape_m3u8("http://www.tg4.ie/en/live/home/")
		elif TG4PreferredStream == "Perma Link":
			return('http://tg4-lh.akamaihd.net/EirBeo1_1200_tg4@118693?videoId=2538842141001&lineUpId;=&pubId=1290862567001&playerId=1364138050001&lineUpId;=&pubId=1290862567001&playerId=1364138050001&affiliateId;=&bandwidthEstimationTest=false&v=3.3.0&fp=WIN_13,0,0,2&r=MWDOQ&g=TPANMNTKXCBN')
	except:
		xbmc.executebuiltin('Notification(TG4, Could not fetch channel URL)')
		
def TV3():
	try:
		if TV3PreferredStream == "AerTV.ie":
			return AerTV("tv3")
		elif TV3PreferredStream == "TV3.ie":
			return scrape_m3u8("http://www.tv3.ie/3player/live/tv3/")
		elif TV3PreferredStream == "Perma Link":
			return('http://csm-e.cds1.yospace.com/csm/extlive/tv3ie01,3e-prd.m3u8')
	except:
		xbmc.executebuiltin('Notification(TV3, Could not fetch channel URL)')

def ThreeE():
	try:
		if ThreeEPreferredStream == "AerTV.ie":
			return AerTV("3e")
		elif ThreeEPreferredStream == "TV3.ie":
			return scrape_m3u8("http://www.tv3.ie/3player/live/3e/")
		elif ThreeEPreferredStream == "Perma Link":
			return('http://csm-e.cds1.yospace.com/csm/extlive/tv3ie01,3e-prd.m3u8')
	except:
		xbmc.executebuiltin('Notification(3e, Could not fetch channel URL)')

def RTENewsNow():
	try:
		if RTENewsNowPreferredStream == "AerTV.ie":
			return AerTV("rte-news-now")
		elif RTENewsNowPreferredStream == "Perma Link":
			return("http://wmsrtsp1.rte.ie/live/android.sdp/playlist.m3u8")
	except:
		xbmc.executebuiltin('Notification(RTE News Now, Could not fetch channel URL)')
        
def UTV():
	try:
		if UTVPreferredStream == "UTV.ie":
			return scrape_m3u8("http://player.utv.ie/live/")
		elif UTVPreferredStream == "ITV.com":
			return scrape_m3u8("http://www.itv.com/utils/ios/ITV_Mobile_Simulcast_Config.xml")
		elif UTVPreferredStream == "Perma Link":
			return("https://itv1liveios-i.akamaihd.net/hls/live/203437/itvlive/ITV1MN/master.m3u8")
	except:
		xbmc.executebuiltin('Notification(UTV Error, Could not fetch channel URL)')

def IrishTV():
	try:
		return scrape_m3u8("http://www.irishtv.ie/playertest.html")
	except:
		xbmc.executebuiltin('Notification(Irish TV Error, Could not fetch channel URL)')
		
def OireachtasTV():
	try:
		return scrape_m3u8("https://media.heanet.ie/player/oirtv.php")
	except:
		xbmc.executebuiltin('Notification(Oireachtas TV Error, Could not fetch channel URL)')
# --------------------------------------------------------------------------------

def streams():
    return [
{'name': parse('RTE One'), 'thumb': path+'resources/logos/RTE1.png', 'link': AerTV("rte-one")},
{'name': parse('RTE One +1'), 'thumb': path+'resources/logos/RTE1_p1.png', 'link': AerTV("rte-one1")},
{'name': parse('RTE Two'), 'thumb': path+'resources/logos/RTE2.png', 'link': AerTV("rte-two")},
{'name': parse('RTEjr'), 'thumb': path+'resources/logos/RTEjr.png', 'link': AerTV("rtejr")},
{'name': parse('RTE News Now'), 'thumb': path+'resources/logos/RTE_News_Now.png', 'link': RTENewsNow()},
{'name': parse('UTV'), 'thumb': path+'resources/logos/UTV.png', 'link': UTV()},
{'name': parse('TV3'), 'thumb': path+'resources/logos/TV3.png', 'link': TV3()},
{'name': parse('3e'), 'thumb': path+'resources/logos/3e.png', 'link': ThreeE()},
{'name': parse('tg4'), 'thumb': path+'resources/logos/TG4.png', 'link': TG4()},
{'name': parse('Irish TV'), 'thumb': path+'resources/logos/IrishTV.png', 'link': IrishTV()},
{'name': parse('Oireachtas TV'), 'thumb': path+'resources/logos/Oireachtas.png', 'link': OireachtasTV()}
]

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

if __name__ == '__main__':
    router(sys.argv[2])