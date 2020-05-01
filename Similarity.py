from Utils import *


# dh.UpdateDB()

def FindSimilar(Song, SongMode="Path", SimilarityMode="Permissive"):
    dh = DatabaseHandler()
    db = dh.GetDB()
    excelFlag = 1
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
    TitleList = []
    SongSpecList = []
    SongFeaturesList = []
    VocalsSpecList = []
    VocalsFeaturesList = []
    MusicsSpecList = []
    MusicFeaturesList = []
    ResultsList = []
    for Song in db.all():
        Title = Song['Title']
        Artist = Song['Artist']
        TitleList.append(Title)
        print(colored("For Song:", "yellow"), colored(f"{Title}", "magenta"))
        SongSpec = ArraySimilarity(SpecHash, Song['SongSpecHash'], SimilarityMode)
        SongSpecList.append(SongSpec)
        SongFeatures = ArraySimilarity(FeaturesHash, Song['SongFeaturesHash'], SimilarityMode)
        SongFeaturesList.append(SongFeatures)
        VocalsSpec = ArraySimilarity(SpecHash, Song['VocalsSpecHash'], SimilarityMode)
        VocalsSpecList.append(VocalsSpec)
        VocalsFeatures = ArraySimilarity(FeaturesHash, Song['VocalsFeaturesHash'], SimilarityMode)
        VocalsFeaturesList.append(VocalsFeatures)
        MusicSpec = ArraySimilarity(SpecHash, Song['MusicSpecHash'], SimilarityMode)
        MusicsSpecList.append(MusicSpec)
        MusicFeatures = ArraySimilarity(FeaturesHash, Song['MusicFeaturesHash'], SimilarityMode)
        MusicFeaturesList.append(MusicFeatures)
        # print(colored(f"Song Spec Similarity {SongSpec} %",
        #               "green"))
        # print(colored(f"Song Features Similarity {SongFeatures} %",
        #               "cyan"))
        # print(colored(f"Vocals Spec Similarity {VocalsSpec} %",
        #               "green"))
        # print(colored(f"Vocals Features Similarity {VocalsFeatures} %",
        #               "cyan"))
        # print(colored(f"Music Spec Similarity {MusicSpec} %",
        #               "green"))
        # print(colored(f"Music Features Similarity {MusicFeatures} %",
        #               "cyan"))
        total = 0.5 * (SongSpec + SongFeatures) + 1.5 * (VocalsSpec + VocalsFeatures) + MusicSpec + MusicFeatures
        ResultsList.append(total)
        print(colored(f"Similarity Index {total} ",
                      "red"))
        SimilarSongs.append([Title, Artist, total])
    # df = pd.DataFrame({'SongName': TitleList,
    #                    'Song Spec': SongSpecList,
    #                    'Song Features': SongFeaturesList,
    #                    'Vocals Spec': VocalsSpecList,
    #                    'Vocals Features': VocalsFeaturesList,
    #                    'Music Spec': MusicsSpecList,
    #                    'Music Features': MusicFeaturesList,
    #                    'Total': ResultsList})
    #
    # if excelFlag == 1:
    #     writer = ExcelWriter('SimilaritySheet.xlsx')
    #     df.to_excel(writer, 'Sheet1', index=False)
    #     writer.save()
    return sorted(SimilarSongs, key=lambda song: song[2], reverse=True)


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

# mixture = mix("amr1.mp3", "sia1.mp3", 0.8)
# res = FindSimilar("Songs/Amrdiab_wahshteny_17.mp3", SongMode="Path", SimilarityMode="Permissive")
# print(res)
