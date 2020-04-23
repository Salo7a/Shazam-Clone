import os
import re
from difflib import SequenceMatcher

import eyed3
import imagehash
from PIL import Image
from tinydb import TinyDB, Query


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


def HashArray(arr):
    im = Image.fromarray(arr)
    hashres = imagehash.phash(arr)
    return hashres


class DatabaseHandler:
    def __init__(self):
        self.number_length = 2
        self.pattern = r"\D(\d{%d})\D" % self.number_length  # \D to avoid matching 567
        self.db = TinyDB('SongsDB.json')
        self.directory = 'Songs'
        self.Songs = []
        self.Music = []
        self.Vocals = []

    def UpdateDB(self):

        for filename in os.listdir(self.directory):
            if "music" in filename.casefold() or "_m_" in filename.casefold() or "accompaniment" in filename.casefold():
                self.Music.append(filename)
            elif "vocal" in filename.casefold() or "_v_" in filename.casefold():
                self.Vocals.append(filename)
            else:
                self.Songs.append(filename)

        for i in range(len(self.Songs)):
            Check = Query()
            if not self.db.search(Check.SongFile == self.Songs[i]):
                Team = re.findall(self.pattern, self.Songs[i])
                File = eyed3.load('Songs/' + self.Songs[i])
                Title = File.tag.title
                Artist = File.tag.artist
                Album = File.tag.album
                MusicFile = self.FindSimilar(i, self.Music)
                VocalsFile = self.FindSimilar(i, self.Vocals)
                if Team:
                    self.db.insert(
                        {'Title': Title, 'Artist': Artist, 'Album': Album, 'TeamNo': Team[0], 'SongFile': self.Songs[i],
                         'MusicFile': MusicFile, 'VocalsFile': VocalsFile})
                else:
                    self.db.insert(
                        {'Title': Title, 'Artist': Artist, 'Album': Album, 'TeamNo': '21', 'SongFile': self.Songs[i],
                         'MusicFile': MusicFile, 'VocalsFile': VocalsFile})

    def FindSimilar(self, i, Matcher):
        if similar(self.Songs[i], Matcher[i]) > 0.7:
            return Matcher[i]
        else:
            for x in Matcher:
                if similar(self.Songs[i], x) > 0.7:
                    return x
            return ""
