# -*- coding: utf-8 -*-
# Module: default
# Author: MathsGrinds
# Created on: 03.04.2016
# License: GPL v.3 https://www.gnu.org/copyleft/gpl.html

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

def str2bool(v):
   return v.lower() in ("yes", "true", "t", "1")

#Settings
addon = xbmcaddon.Addon()

Guide = str2bool(addon.getSetting('guide'))
RTENewsNowPreferredStream = str(addon.getSetting('RTENewsNowpreferredstream'))
TG4PreferredStream = str(addon.getSetting('TG4preferredstream'))
TV3PreferredStream = str(addon.getSetting('TV3preferredstream'))
ThreeEPreferredStream = str(addon.getSetting('ThreeEpreferredstream'))
be3PreferredStream = str(addon.getSetting('be3preferredstream'))
quality = str(addon.getSetting('quality'))

email = str(addon.getSetting('email'))
password = str(addon.getSetting('password'))

useragent = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0'}

__url__ = sys.argv[0]
__handle__ = int(sys.argv[1])
path = sys.path[0]+"/"

def login():
   try:
      #xbmc.executebuiltin('Notification(Login, Trying username and password)')
      #Load a Pre-Defined Account;
      usernames = ["walshmary1473182935@gmail.com ","walshmary1473182029@gmail.com ","walshmary1473181167@gmail.com ","walshmary1473180237@gmail.com ","walshmary1473179338@gmail.com ","walshmary1473178433@gmail.com ","walshmary1473177532@gmail.com ","walshmary1473176634@gmail.com ","walshmary1473175762@gmail.com ","walshmary1473174909@gmail.com ","walshmary1473174128@gmail.com ","walshmary1473173034@gmail.com ","walshmary1473172161@gmail.com ","walshmary1473171226@gmail.com ","walshmary1473170332@gmail.com ","walshmary1473169502@gmail.com ","walshmary1473168526@gmail.com ","walshmary1473167631@gmail.com ","walshmary1473166811@gmail.com ","walshmary1473165949@gmail.com ","walshmary1473165005@gmail.com ","walshmary1473164027@gmail.com ","walshmary1473163192@gmail.com ","walshmary1473162231@gmail.com ","walshmary1473161333@gmail.com ","walshmary1473160429@gmail.com ","walshmary1473159529@gmail.com ","walshmary1473158631@gmail.com ","walshmary1473157729@gmail.com ","walshmary1473156827@gmail.com ","walshmary1473155928@gmail.com ","walshmary1473155031@gmail.com ","walshmary1473154130@gmail.com ","walshmary1473153224@gmail.com ","walshmary1473152391@gmail.com ","walshmary1473151429@gmail.com ","walshmary1473150532@gmail.com ","walshmary1473149767@gmail.com ","walshmary1473148796@gmail.com ","walshmary1473147827@gmail.com ","walshmary1473146999@gmail.com ","walshmary1473146065@gmail.com ","walshmary1473145127@gmail.com ","walshmary1473144227@gmail.com ","walshmary1473143331@gmail.com ","walshmary1473142491@gmail.com ","walshmary1473141526@gmail.com ","walshmary1473140634@gmail.com ","walshmary1473139731@gmail.com ","walshmary1473138833@gmail.com ","walshmary1473137928@gmail.com ","walshmary1473137029@gmail.com ","walshmary1473136132@gmail.com ","walshmary1473135235@gmail.com ","walshmary1473134330@gmail.com ","walshmary1473133461@gmail.com ","walshmary1473132527@gmail.com ","walshmary1473131735@gmail.com ","walshmary1473130726@gmail.com ","walshmary1473129976@gmail.com ","walshmary1473128927@gmail.com ","walshmary1473128033@gmail.com ","walshmary1473127128@gmail.com ","walshmary1473126239@gmail.com ","walshmary1473124505@gmail.com ","walshmary1473123527@gmail.com ","walshmary1473122704@gmail.com ","walshmary1473121729@gmail.com ","walshmary1473120830@gmail.com ","walshmary1473119998@gmail.com ","walshmary1473119070@gmail.com ","walshmary1473118124@gmail.com ","walshmary1473117233@gmail.com ","walshmary1473116331@gmail.com ","walshmary1473115428@gmail.com ","walshmary1473114528@gmail.com ","walshmary1473113627@gmail.com ","walshmary1473112727@gmail.com ","walshmary1473111824@gmail.com ","walshmary1473110034@gmail.com ","walshmary1473109136@gmail.com ","walshmary1473107329@gmail.com ","walshmary1473107237@gmail.com ","walshmary1473104170@gmail.com ","walshmary1473102555@gmail.com ","walshmary1473101954@gmail.com ","walshmary1473101570@gmail.com ","walshmary1473100758@gmail.com ","walshmary1473100148@gmail.com ","walshmary1473099659@gmail.com ","walshmary1473099156@gmail.com ","walshmary1473098346@gmail.com ","walshmary1473097859@gmail.com ","walshmary1473097261@gmail.com ","walshmary1473096549@gmail.com ","walshmary1473095959@gmail.com ","walshmary1473095572@gmail.com ","walshmary1473094751@gmail.com ","walshmary1473094264@gmail.com ","walshmary1473093556@gmail.com ","walshmary1473092954@gmail.com ","walshmary1473092351@gmail.com ","walshmary1473092042@gmail.com ","walshmary1473091156@gmail.com ","walshmary1473090552@gmail.com ","walshmary1473090284@gmail.com ","walshmary1473089615@gmail.com ","walshmary1473088855@gmail.com ","walshmary1473088153@gmail.com ","walshmary1473087554@gmail.com ","walshmary1473086955@gmail.com ","walshmary1473086349@gmail.com ","walshmary1473085861@gmail.com ","walshmary1473085152@gmail.com ","walshmary1473084586@gmail.com ","walshmary1473083964@gmail.com ","walshmary1473083465@gmail.com ","walshmary1473082866@gmail.com ","walshmary1473082441@gmail.com ","walshmary1473081659@gmail.com ","walshmary1473080951@gmail.com ","walshmary1473080349@gmail.com ","walshmary1473079748@gmail.com ","walshmary1473079152@gmail.com ","walshmary1473078555@gmail.com ","walshmary1473078102@gmail.com ","walshmary1473077683@gmail.com ","walshmary1473076755@gmail.com ","walshmary1473076268@gmail.com ","walshmary1473075662@gmail.com ","walshmary1473075166@gmail.com ","walshmary1473074348@gmail.com ","walshmary1473073757@gmail.com ","walshmary1473073154@gmail.com ","walshmary1473072659@gmail.com ","walshmary1473072065@gmail.com ","walshmary1473071354@gmail.com ","walshmary1473070862@gmail.com ","walshmary1473070151@gmail.com ","walshmary1473069651@gmail.com ","walshmary1473069053@gmail.com ","walshmary1473068460@gmail.com","walshmary1473067749@gmail.com","walshmary1473067265@gmail.com","walshmary1473066550@gmail.com"]
      t = (int((60*int(strftime("%H",gmtime()))+int(strftime("%M",gmtime())))/10))%144
      pre_defined_email = usernames[t]
      pre_defined_password = "Password0"

      #If there isn't both Email and Password set;
      if not email and not password:
           
         #Use a Pre-Defined Free Account;
         req = urllib2.Request('http://api.aertv.ie/v2/users/login', urllib.urlencode({'email':pre_defined_email, 'password':pre_defined_password}), useragent)
               
      else:
        
         #Use the Account defined in Settings by the User;
         req = urllib2.Request('http://api.aertv.ie/v2/users/login', urllib.urlencode({'email':email, 'password':password}), useragent)
               
      #Output the JSON;
      html = urllib2.urlopen(req).read()
      return json.loads(html)
        
   except:
    
      #Notify the user that the Email and Password is incorrect;
      xbmc.executebuiltin('Notification(Login Failed, username and/or password is incorrect.)')
      return ""

#Login;
loginj = login()

def AerTV(channel):
    
    #Get the JSON from the Players API;
    req = urllib2.Request("http://api.aertv.ie/v2/players/"+channel+"?user_token="+loginj[u'data'][u'user_token'], None, useragent)
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
   try:
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
           elif channel=="Dail":
               return " - Parliamentary Television" #also breaks out of def;
           elif channel=="Seanad":
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
           elif channel=="be3":
               url='http://entertainment.ie/tv/display.asp?channelid=1929'
           
           #Parse the show for the Entertainment.ie links;
           req = urllib2.Request(url, None, useragent)
           html = urllib2.urlopen(req).read()
           try:
               return " - " + re.findall('title=\".*\" onclick', html)[0].replace('title="','').replace('" onclick','').replace('View ','').replace(' programme details','').replace("&amp;", "and").replace(" & "," and ").replace('and#39;', ' ').replace('&Aacute;', 'A').replace('&Eacute;', 'E').replace('&Iacute;', 'I').replace('&Oacute;', 'O').replace('&Uacute;', 'U').replace('&aacute;', 'a').replace('&eacute;', 'e').replace('&iacute;', 'i').replace('&oacute;', 'o').replace('&uacute;', 'u')
           except:
               return " - Close"
       else:
           return ""
   except:
      return "No guide info"

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
   except:
      xbmc.executebuiltin('Notification(TG4, Could not fetch channel URL)')
      return("")
      
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
      return("")

def be3():
   try:
      if be3PreferredStream == "TV3.ie":
         return scrape_m3u8("http://www.tv3.ie/3player/live/be3/")
      elif be3PreferredStream == "Perma Link":
         return('http://csm-e.cds1.yospace.com/csm/extlive/tv3ie01,be3-prd.m3u8')
   except:
      xbmc.executebuiltin('Notification(be3, Could not fetch channel be3)')
      return("")     

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
      return("")

def RTENewsNow():
   try:
      if RTENewsNowPreferredStream == "AerTV.ie":
         return AerTV("rte-news-now")
      elif RTENewsNowPreferredStream == "Perma Link":
         return("http://wmsrtsp1.rte.ie/live/android.sdp/playlist.m3u8")
   except:
      xbmc.executebuiltin('Notification(RTE News Now, Could not fetch channel URL)')
      return("")
        
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
      return("")

def IrishTV():
   try:
      return scrape_m3u8("http://www.irishtv.ie/playertest.html")
   except:
      xbmc.executebuiltin('Notification(Irish TV Error, Could not fetch channel URL)')
      return("")

def OireachtasTV():
   try:
      return "https://media.heanet.ie/oirlive/oireachtas/ngrp:oireachtas.stream_all/playlist.m3u8"
   except:
      xbmc.executebuiltin('Notification(Oireachtas TV Error, Could not fetch channel URL)')
      return("")
     
def Dail():
   try:
      return "https://media.heanet.ie/oirlive/dail/ngrp:dail.stream_all/playlist.m3u8"
   except:
      xbmc.executebuiltin('Notification(Oireachtas TV Error, Could not fetch channel URL)')
      return("")
      
def Seanad():
   try:
      return "https://media.heanet.ie/oirlive/seanad/ngrp:seanad.stream_all/playlist.m3u8"
   except:
      xbmc.executebuiltin('Notification(Oireachtas TV Error, Could not fetch channel URL)')
      return("")
# --------------------------------------------------------------------------------

def streams():
    return [
{'name': parse('RTE One'), 'thumb': path+'resources/logos/RTE1.png', 'link': AerTV('rte-one')},
{'name': parse('RTE Two'), 'thumb': path+'resources/logos/RTE2.png', 'link': AerTV('rte-two')},
{'name': parse('TV3'), 'thumb': path+'resources/logos/TV3.png', 'link': TV3()},
{'name': parse('tg4'), 'thumb': path+'resources/logos/TG4.png', 'link': TG4()},
{'name': parse('3e'), 'thumb': path+'resources/logos/3e.png', 'link': ThreeE()},
{'name': parse('be3'), 'thumb': path+'resources/logos/be3.png', 'link': be3()},
{'name': parse('RTEjr'), 'thumb': path+'resources/logos/RTEjr.png', 'link': AerTV("rtejr")},
{'name': parse('RTE One +1'), 'thumb': path+'resources/logos/RTE1_p1.png', 'link': AerTV("rte-one1")},
{'name': parse('RTE News Now'), 'thumb': path+'resources/logos/RTE_News_Now.png', 'link': RTENewsNow()},
{'name': parse('Oireachtas TV'), 'thumb': path+'resources/logos/Oireachtas.png', 'link': OireachtasTV()},
{'name': parse('Dail'), 'thumb': path+'resources/logos/Dail.png', 'link': Dail()},
{'name': parse('Seanad'), 'thumb': path+'resources/logos/Seanad.png', 'link': Seanad()}
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
