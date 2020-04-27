from Utils import *

dh = DatabaseHandler()
db = dh.GetDB()


# dh.UpdateDB()

def FindSimilar(Song, SongMode="Path", SimilarityMode="Permissive"):
    if SongMode == "Path":
        print(colored(f"Reading File {Song}",
                      "yellow"))
        spectrogram, features = getSpectrogram(Song)
    else:
        print(colored(f"Reading Song Array",
                      "yellow"))
        spectrogram, features = getSpectrogram(Song, "Array")
    SpecHash = HashArray(spectrogram)
    FeaturesHash = HashArray(features)
    print(colored("Beginning Song Detection",
                  "yellow"))
    SimilarSongs = []
    for Song in db.all():
        Title = Song['Title']
        print(colored("For Song:", "yellow"), colored(f"{Title}", "magenta"))
        SongSpec = ArraySimilarity(SpecHash, Song['SongSpecHash'], SimilarityMode)
        SongFeatures = ArraySimilarity(FeaturesHash, Song['SongFeaturesHash'], SimilarityMode)
        VocalsSpec = ArraySimilarity(SpecHash, Song['VocalsSpecHash'], SimilarityMode)
        VocalsFeatures = ArraySimilarity(FeaturesHash, Song['VocalsFeaturesHash'], SimilarityMode)
        MusicSpec = ArraySimilarity(SpecHash, Song['MusicSpecHash'], SimilarityMode)
        MusicFeatures = ArraySimilarity(FeaturesHash, Song['MusicFeaturesHash'], SimilarityMode)
        print(colored(f"Song Spec Similarity {SongSpec} %",
                      "green"))
        print(colored(f"Song Features Similarity {SongFeatures} %",
                      "cyan"))
        print(colored(f"Vocals Spec Similarity {VocalsSpec} %",
                      "green"))
        print(colored(f"Vocals Features Similarity {VocalsFeatures} %",
                      "cyan"))
        print(colored(f"Music Spec Similarity {MusicSpec} %",
                      "green"))
        print(colored(f"Music Features Similarity {MusicFeatures} %",
                      "cyan"))
        total = SongSpec + SongFeatures + VocalsSpec + VocalsFeatures + MusicSpec + MusicFeatures
        print(colored(f"Similarity Index {total} ",
                      "red"))
        SimilarSongs.append([Title, total])
    return np.asarray(SimilarSongs)


def ArraySimilarity(Arr1, Arr2, Mode="Permissive"):
    Hash1 = np.asarray(Arr1)
    Hash2 = np.asarray(Arr2)
    if len(Hash1) != 0 and len(Hash2) != 0:
        if Mode == "Permissive":
            percentage = len(set(Hash1[:, 0]) & set(Hash2[:, 0])) / float(
                len(set(Hash1[:, 0]) | set(Hash2[:, 0]))) * 100
        else:
            Hash1 = [(x, y) for x, y in Hash1]
            Hash2 = [(x, y) for x, y in Hash2]
            percentage = len(set(Hash1) & set(Hash2)) / float(len(set(Hash1) | set(Hash2))) * 100
    else:
        percentage = 0
    # number_of_equal_elements = np.sum(Arr1 == Arr2)
    # total_elements = np.multiply(*Arr1.shape)
    # percentage = number_of_equal_elements / total_elements

    return percentage


FindSimilar("mix.mp3", "Enforcing")
