import os
import re
from difflib import SequenceMatcher

import eyed3
import imagehash
from PIL import Image
from tinydb import TinyDB, Query

number_length = 2
pattern = r"\D(\d{%d})\D" % number_length  # \D to avoid matching 567

db = TinyDB('SongsDB.json')


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


def HashArray(arr):
    im = Image.fromarray(arr)
    hashres = imagehash.phash(arr)
    return hashres


def UpdateDB():
    directory = 'Songs'
    Songs = []
    Music = []
    Vocals = []
    for filename in os.listdir(directory):
        if "music" in filename.casefold() or "_m_" in filename.casefold() or "accompaniment" in filename.casefold():
            Music.append(filename)
        elif "vocal" in filename.casefold() or "_v_" in filename.casefold():
            Vocals.append(filename)
        else:
            Songs.append(filename)

    for i in range(len(Songs)):
        Check = Query()
        if not db.search(Check.SongFile == Songs[i]):
            Team = re.findall(pattern, Songs[i])
            File = eyed3.load('Songs/' + Songs[i])
            Title = File.tag.title
            Artist = File.tag.artist
            Album = File.tag.album
            if Team:
                db.insert({'Title': Title, 'Artist': Artist, 'Album': Album, 'TeamNo': Team[0], 'SongFile': Songs[i],
                           'MusicFile': Music[i], 'VocalsFile': Vocals[i]})
            else:
                db.insert({'Title': Title, 'Artist': Artist, 'Album': Album, 'TeamNo': '21', 'SongFile': Songs[i],
                           'MusicFile': Music[i], 'VocalsFile': Vocals[i]})
