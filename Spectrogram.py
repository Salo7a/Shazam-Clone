from AudioFunctions import *
from scipy import signal
import matplotlib.pyplot as plt
import librosa
import sklearn
from scipy import spatial
from sklearn.metrics.pairwise import cosine_similarity
import librosa.display

# USE THIS FUNCTION....
def getSpectrogram(path):
    songClass = song2data(path)
    songArray = getFirstData(songClass.data, 60)
    frequencies, times, spectrogram = signal.spectrogram(songArray, 44100)
    melSpectrogram = librosa.feature.melspectrogram(S=spectrogram)
    features = SpectrogramFeatures(melSpectrogram)
    return melSpectrogram, features


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
    features = np.append(mfcc, specCentroids)
    features = np.append(features, specRolls)
    features = np.append(features, polyFeatures)
    features = np.append(features, bandwidth)
    # print(features.shape)
    return features



