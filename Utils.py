import hashlib
import os
import re
from difflib import SequenceMatcher
from operator import itemgetter

import eyed3
import matplotlib.pyplot as plt
import numpy as np
from scipy.ndimage import generate_binary_structure, maximum_filter, binary_erosion, iterate_structure
from termcolor import colored
from tinydb import TinyDB, Query

from Spectrogram import getSpectrogram

IDX_FREQ_I = 0
IDX_TIME_J = 1
DEFAULT_FS = 44100
DEFAULT_WINDOW_SIZE = 4096
DEFAULT_OVERLAP_RATIO = 0.5
DEFAULT_FAN_VALUE = 15
DEFAULT_AMP_MIN = 10
PEAK_NEIGHBORHOOD_SIZE = 20
MIN_HASH_TIME_DELTA = 0
MAX_HASH_TIME_DELTA = 200
PEAK_SORT = True
FINGERPRINT_REDUCTION = 20


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


def HashArray(arr, amp_min=DEFAULT_AMP_MIN, fan_value=DEFAULT_FAN_VALUE):
    peaks = get_2D_peaks(arr, plot=False, amp_min=amp_min)
    return generate_hashes(peaks, fan_value=fan_value)


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
                print("Found Song: " + Title)
                Artist = File.tag.artist
                Album = File.tag.album
                MusicFile = self.FindSimilar(i, self.Music)
                VocalsFile = self.FindSimilar(i, self.Vocals)
                print("Generating Song Hashes")
                SongSpecHash, SongFeaturesHash = self.getHash(self.Songs[i])
                print(colored(f"Generated {len(SongSpecHash)} Spec Hashes & {len(SongFeaturesHash)} Features Hashes"
                              , "green"))
                print("Generating Vocals Hashes")
                VocalsSpecHash, VocalsFeaturesHash = self.getHash(VocalsFile)
                print(colored(f"Generated {len(VocalsSpecHash)} Spec Hashes & {len(VocalsFeaturesHash)} Features Hashes"
                              , "green"))
                print("Generating Music Hashes")
                MusicSpecHash, MusicFeaturesHash = self.getHash(MusicFile)
                print(colored(f"Generated {len(MusicSpecHash)} Spec Hashes & {len(MusicFeaturesHash)} Features Hashes",
                              "green"))
                if not Team:
                    Team[0] = "0"
                self.db.insert(
                    {'Title': Title, 'Artist': Artist, 'Album': Album, 'TeamNo': Team[0], 'SongFile': self.Songs[i],
                     'MusicFile': MusicFile, 'VocalsFile': VocalsFile, "SongSpecHash": SongSpecHash,
                     "SongFeaturesHash": SongFeaturesHash, "VocalsSpecHash": VocalsSpecHash,
                     "VocalsFeaturesHash": VocalsFeaturesHash, "MusicSpecHash": MusicSpecHash,
                     "MusicFeaturesHash": MusicFeaturesHash})

    def FindSimilar(self, i, Matcher):
        if similar(self.Songs[i], Matcher[i]) > 0.7:
            return Matcher[i]
        else:
            for x in Matcher:
                if similar(self.Songs[i], x) > 0.7:
                    return x
            return ""

    def GetDB(self):
        return self.db

    def getHash(self, file):
        spec, features = getSpectrogram(self.directory + "/" + file)
        return HashArray(spec), HashArray(features)

    def GetDifferences(self):
        Data = self.db.all()
        for song in Data:
            for song2 in Data:
                # s1 = imagehash.hex_to_hash(song['SongSpecHash'])
                # s2 = imagehash.hex_to_hash(song2['SongSpecHash'])
                # diff = s1 - s2
                # print("SongSpecHash Difference Between " + song['Title'] + " & " + song2['Title'] + " = " + str(diff))
                # s1 = imagehash.hex_to_hash(song['SongFeaturesHash'])
                # s2 = imagehash.hex_to_hash(song2['SongFeaturesHash'])
                # diff = s1 - s2
                # print(
                #     "SongFeaturesHash Difference Between " + song['Title'] + " & " + song2['Title'] + " = " + str(diff))
                # s1 = imagehash.hex_to_hash(song['VocalsSpecHash'])
                # s2 = imagehash.hex_to_hash(song2['VocalsSpecHash'])
                # diff = s1 - s2
                # print("VocalsSpecHash Difference Between " + song['Title'] + " & " + song2['Title'] + " = " + str(diff))
                # s1 = imagehash.hex_to_hash(song['VocalsFeaturesHash'])
                # s2 = imagehash.hex_to_hash(song2['VocalsFeaturesHash'])
                # diff = s1 - s2
                # print("VocalsFeaturesHash Difference Between " + song['Title'] + " & " + song2['Title'] + " = " + str(
                #     diff))
                # s1 = imagehash.hex_to_hash(song['MusicSpecHash'])
                # s2 = imagehash.hex_to_hash(song2['MusicSpecHash'])
                # diff = s1 - s2
                # print("MusicSpecHash Difference Between " + song['Title'] + " & " + song2['Title'] + " = " + str(diff))
                # s1 = imagehash.hex_to_hash(song['MusicFeaturesHash'])
                # s2 = imagehash.hex_to_hash(song2['MusicFeaturesHash'])
                # diff = s1 - s2
                # print("MusicFeaturesHash Difference Between " + song['Title'] + " & " + song2['Title'] + " = " + str(
                #     diff))
                pass


def get_2D_peaks(arr2D, plot=False, amp_min=DEFAULT_AMP_MIN):
    # http://docs.scipy.org/doc/scipy/reference/generated/scipy.ndimage.morphology.iterate_structure.html#scipy.ndimage.morphology.iterate_structure
    struct = generate_binary_structure(2, 1)
    neighborhood = iterate_structure(struct, PEAK_NEIGHBORHOOD_SIZE)

    # find local maxima using our fliter shape
    local_max = maximum_filter(arr2D, footprint=neighborhood) == arr2D
    background = (arr2D == 0)
    eroded_background = binary_erosion(background, structure=neighborhood,
                                       border_value=1)

    # Boolean mask of arr2D with True at peaks
    detected_peaks = local_max ^ eroded_background

    # extract peaks
    amps = arr2D[detected_peaks]
    j, i = np.where(detected_peaks)

    # filter peaks
    amps = amps.flatten()
    peaks = zip(i, j, amps)
    peaks_filtered = [x for x in peaks if x[2] > amp_min]  # freq, time, amp

    # get indices for frequency and time
    frequency_idx = [x[1] for x in peaks_filtered]
    time_idx = [x[0] for x in peaks_filtered]

    # scatter of the peaks
    if plot:
        fig, ax = plt.subplots()
        ax.imshow(arr2D)
        ax.scatter(time_idx, frequency_idx)
        ax.set_xlabel('Time')
        ax.set_ylabel('Frequency')
        ax.set_title("Spectrogram")
        plt.gca().invert_yaxis()
        plt.show()

    return list(zip(frequency_idx, time_idx))


def generate_hashes(peaks, fan_value=DEFAULT_FAN_VALUE):
    """
    Hash list structure:
       sha1_hash[0:20]    time_offset
    [(e05b341a9b77a51fd26, 32), ... ]
    """
    if PEAK_SORT:
        peaks.sort(key=itemgetter(1))
    hashes = []
    for i in range(len(peaks)):
        for j in range(1, fan_value):
            if (i + j) < len(peaks):

                freq1 = peaks[i][IDX_FREQ_I]
                freq2 = peaks[i + j][IDX_FREQ_I]
                t1 = peaks[i][IDX_TIME_J]
                t2 = peaks[i + j][IDX_TIME_J]
                t_delta = t2 - t1

                if MIN_HASH_TIME_DELTA <= t_delta <= MAX_HASH_TIME_DELTA:
                    h = hashlib.sha1(("%s|%s|%s" % (
                        str(freq1).encode('utf-8'), str(freq2).encode('utf-8'), str(t_delta).encode('utf-8'))).encode(
                        'utf-8'))
                    # yield (h.hexdigest()[0:FINGERPRINT_REDUCTION], t1)
                    hashes.append((h.hexdigest()[0:FINGERPRINT_REDUCTION], int(t1)))
    return hashes
