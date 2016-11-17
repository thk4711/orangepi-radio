#!/usr/bin/python

import re
from mpd import MPDClient, MPDError, CommandError
stations = None

#---------------------------------------------------#
#        init mpd                                   #
#---------------------------------------------------#
def init(host="localhost", port=6600, playlist="radio", columns=200):
    global mpd_client
    global mpd_host
    global mpd_port
    global diplay_columns
    global stations
    mpd_host = host
    mpd_port = port
    diplay_columns = columns
    mpd_client = MPDClient()
    mpd_client.timeout = 20
    mpd_client.idletimeout = None
    mpd_client.connect(mpd_host, mpd_port)
    mpd_client.clear()
    mpd_client.load(playlist)
    mpd_client.play(0)
    stations = mpd_client.playlistinfo()
    mpd_client.disconnect()

#---------------------------------------------------------------------#
#      Get infos about the current stream from mpd                    #
#---------------------------------------------------------------------#
def info():
    title  = ""
    artist = ""
    name   = ""
    pos    = 0
    mpd_client.connect(mpd_host, mpd_port)
    info = mpd_client.currentsong()
    if 'name' in info.keys():
        name = info["name"]
        name = name[:diplay_columns]
        name = name.strip()
    if 'title'in info.keys():
        parts  = re.split("( \- )", info["title"], 2)
        if len(parts) > 1:
            artist=parts[0]
            title=parts[2]
        else:
            artist = info["title"]
    if 'pos' in info.keys():
        pos = int(info["pos"])
    artist=artist.replace(name, "")
    artist= artist[:diplay_columns]
    artist=artist.strip()
    title=title.replace(name, "")
    title=title[:diplay_columns]
    title=title.strip()
    mpd_client.disconnect()
    return(name, artist, title, pos)

#---------------------------------------------------------------------#
#      tune to a station                                              #
#---------------------------------------------------------------------#
def play(station):
    mpd_client.connect(mpd_host, mpd_port)
    mpd_client.play(station)
    mpd_client.disconnect()

#---------------------------------------------------------------------#
#      stop mpd                                                       #
#---------------------------------------------------------------------#
def stop():
    mpd_client.connect(mpd_host, mpd_port)
    mpd_client.stop()
    mpd_client.disconnect()

#---------------------------------------------------------------------#
#      Get status from mpd                                            #
#---------------------------------------------------------------------#
def stat():
    mpd_client.connect(mpd_host, mpd_port)
    status = mpd_client.status()
    mpd_client.disconnect()
    return status['state']
