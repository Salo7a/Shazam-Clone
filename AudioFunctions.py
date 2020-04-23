import numpy as np
from numpy.fft import fft, ifft
from pydub import AudioSegment


class SongData():
    def __init__(self, path):
        self.audio = AudioSegment.from_file(path).set_channels(1)
        self.rate, self.data = self.audio.frame_rate, np.array(self.audio.get_array_of_samples())
        self.length = len(self.data)
        self.duration = self.audio.duration_seconds
        self.time = np.linspace(0, self.duration, self.length)
        self.freq = np.linspace(0, self.rate / 2, int(self.length / 2))
        self.fftArray = fft(self.data)
        self.fftArrayPositive = self.fftArray[:self.length // 2]
        self.fftArrayNegative = np.flip(self.fftArray[self.length // 2:])
        self.fftArrayAbs = np.abs(self.fftArray)
        self.fftPlotting = self.fftArrayAbs[: self.length // 2]


def song2data(path):
    songClass = SongData(path)
    return songClass


def data2wav(arr):
    # print(arr)
    data = ifft(arr, len(arr)).real
    return data.astype(np.int32)


def getFirstData(songArr, time):
    selectedData = songArr[:int(time*44100)]
    return selectedData


def similarityIndex(vA, vB):
    sim = np.dot(vA, vB)/(np.sqrt(np.dot(vA, vA)) * np.sqrt(np.dot(vB, vB)))
    return sim
