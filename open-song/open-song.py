#!/usr/bin/env python3

import os
import platform
import sys
import requests
import re
from bs4 import BeautifulSoup

YOUTUBE_BASE = 'https://www.youtube.com'
TARGET_CLASS = 'yt-simple-endpoint style-scope ytd-video-renderer'

def get_song_links(song):
    song_links = []
    search_query = '/results?search_query='
    song = song.replace(' ', '+')
    search_url = YOUTUBE_BASE + search_query + song
    yt_response = requests.get(search_url)
    soup = BeautifulSoup(yt_response.text, 'html.parser')
    start_indices = [res.start() for res in re.finditer('/watch?', str(soup))]

    for index in start_indices:
        link = str(soup)[index:index + 20]

        if '?v=' in link:
            song_links.append(YOUTUBE_BASE + link)

    return [search_url] + song_links


def get_open_command():
    os_name = platform.system()
    if os_name == 'Linux':
        return 'xdg-open'
    if os_name == 'Darwin':
        return 'open'
    if os_name == 'Windows':
        return 'start'


def get_song_names():
    args = sys.argv
    song_names = args[1:]
    return song_names

def open_url(open_command, link):
    open_p = os.system('{} {}'.format(open_command, link))

def open_target_links(song, ong_links):
    open_command = get_open_command()
    print('For song ' + song)
    print (
'''
Enter one of these
1. Open search results
2. Open first result on youtube
3. Open top five results
or other key/s to exit
'''
    )

    choice = int(input())
    if choice not in [1, 2, 3]:
        sys.exit(-1)
    else:
        if choice == 1:
            open_url(open_command, song_links[0])
        elif choice == 2:
            open_url(open_command, song_links[1])
        else:
            for link in song_links[1:6]:
                open_url(open_command, link)


if (__name__ == '__main__'):
    song_names = get_song_names()
    for song in song_names:
        song_links = get_song_links(song)
        open_target_links(song, song_links)

    sys.exit(-1)
