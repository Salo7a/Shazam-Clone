from Utils import *

dh = DatabaseHandler()
db = dh.GetDB()


# dh.UpdateDB()

def FindSimilar(Path):
    spectrogram, features = getSpectrogram(Path)
    SpecHash = HashArray(spectrogram)
    FeaturesHash = HashArray(features)
    print(colored("Beginning Song Detection",
                  "yellow"))
    for Song in db.all():
        Title = Song['Title']
        print(colored("For Song:", "yellow"), colored(f"{Title}", "magenta"))
        SongSpec = ArraySimilarity(SpecHash, Song['SongSpecHash'])
        SongFeatures = ArraySimilarity(FeaturesHash, Song['SongFeaturesHash'])
        VocalsSpec = ArraySimilarity(SpecHash, Song['VocalsSpecHash'])
        VocalsFeatures = ArraySimilarity(FeaturesHash, Song['VocalsFeaturesHash'])
        MusicSpec = ArraySimilarity(SpecHash, Song['MusicSpecHash'])
        MusicFeatures = ArraySimilarity(FeaturesHash, Song['MusicFeaturesHash'])
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


def ArraySimilarity(Arr1, Arr2):
    Hash1 = np.asarray(Arr1)
    Hash2 = np.asarray(Arr2)
    # number_of_equal_elements = np.sum(Arr1 == Arr2)
    # total_elements = np.multiply(*Arr1.shape)
    # percentage = number_of_equal_elements / total_elements
    percentage = len(set(Hash1[:, 0]) & set(Hash2[:, 0])) / float(len(set(Hash1[:, 0]) | set(Hash2[:, 0]))) * 100
    return percentage


FindSimilar("Songs/mix.mp3")
