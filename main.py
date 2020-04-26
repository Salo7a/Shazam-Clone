from Utils import *

dh = DatabaseHandler()
db = dh.GetDB()


# dh.UpdateDB()

def FindSimilar(Path):
    print(colored(f"Reading File {Path}",
                  "yellow"))
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


def ArraySimilarity(Arr1, Arr2, Mode="Permissive"):
    Hash1 = np.asarray(Arr1)
    Hash2 = np.asarray(Arr2)
    if len(Hash1) != 0 and len(Hash2) != 0:
        if Mode == "Permissive":
            percentage = len(set(Hash1[:, 0]) & set(Hash2[:, 0])) / float(len(set(Hash1[:, 0]) | set(Hash2[:, 0]))) * 100
        else:
            percentage = len(set(Hash1) & set(Hash2)) / float(len(set(Hash1) | set(Hash2))) * 100
    else:
        percentage = 0
    # number_of_equal_elements = np.sum(Arr1 == Arr2)
    # total_elements = np.multiply(*Arr1.shape)
    # percentage = number_of_equal_elements / total_elements

    return percentage


FindSimilar("Songs/Amrdiab_wahshteny_vocals_17.mp3")
