import librosa
import librosa.display
from scipy import signal

from AudioFunctions import *
from Utils import *


# USE THIS FUNCTION....
def getSpectrogram(path):
    songClass = song2data(path)
    songArray = getFirstData(songClass.data, 60)
    frequencies, times, spectrogram = signal.spectrogram(songArray, 44100, window="hanning", nperseg=4096,
                                                         noverlap=2048,
                                                         nfft=4096)
    features = SpectrogramFeatures(spectrogram)
    spectrogram = 10 * np.log10(spectrogram)
    spectrogram[spectrogram == -np.inf] = 0
    features = 10 * np.log10(features)
    features[features == -np.inf] = 0

    return spectrogram, features, times


def MFCC(spectrogram):
    # S = librosa.feature.melspectrogram(S=spectrogram)
    mfcc = librosa.feature.mfcc(S=spectrogram)
    print(mfcc.shape)
    return mfcc


def SpectralCentroid(spectrogram):
    # S = librosa.feature.melspectrogram(S=spectrogram)
    spectCentroids = librosa.feature.spectral_centroid(S=spectrogram)
    print(spectCentroids.shape)
    return spectCentroids


def SpectralRollOff(spectrogram):
    # S = librosa.feature.melspectrogram(S=spectrogram)
    specRolls = librosa.feature.spectral_rolloff(S=spectrogram)
    print(specRolls.shape)
    return specRolls


def PolyFeatures(spectrogram):
    # S = librosa.feature.melspectrogram(S=spectrogram)
    polyFeatures = librosa.feature.poly_features(S=spectrogram, order=2)
    print(polyFeatures.shape)
    return polyFeatures


def SpectralBandwidth(spectrogram):
    # S = librosa.feature.melspectrogram(S=spectrogram)
    bandwidth = librosa.feature.spectral_bandwidth(S=spectrogram)
    return bandwidth


def SpectrogramFeatures(spectrogram):
    mfcc = MFCC(spectrogram)
    specCentroids = SpectralCentroid(spectrogram)
    specRolls = SpectralRollOff(spectrogram)
    polyFeatures = PolyFeatures(spectrogram)
    bandwidth = SpectralBandwidth(spectrogram)
    features = np.concatenate((mfcc, specCentroids))
    features = np.concatenate((features, specRolls))
    features = np.concatenate((features, polyFeatures))
    features = np.concatenate((features, bandwidth))
    # print(features.shape)
    return features


dh = DatabaseHandler()
db = dh.GetDB()
Song = Query()
test = db.get(Song.TeamNo == "17")
MusicSpec, MusicFeatures, times = getSpectrogram("Songs/" + test['MusicFile'])
MusicSpecHash = HashArray(MusicSpec)
# SongFeaturesHash = HashArray(MusicFeatures)
# db.update({"MusicSpecHash": str(MusicSpecHash)}, Song.MusicFile == test['MusicFile'])
# test2 = db.get(Song.TeamNo == "21")
# t1 = hex_to_hash(test2['MusicSpecHash'])
# t2 = hex_to_hash(test2['SongSpecHash'])
# t3 = MusicSpecHash
