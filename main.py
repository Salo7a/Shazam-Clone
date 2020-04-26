from Spectrogram import *

DH = DatabaseHandler()
DH.UpdateDB()
DH.GetDifferences()
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
