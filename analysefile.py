import librosa
import numpy as np

OPTION = "mfcc" #  mfcc or mels (melspectrogram)

GENRES = 10 #  number of genres available

sr = 22050 #  Sample rate
DURATION = 25
SPT = sr * DURATION #  num of samples per track

SEGMENTS = 10
SPS = int(SPT / SEGMENTS) #  num of samples in each segment

N_MFCC = 13 #  for MFCCs
N_MELS = 128 #  for melspecs


def prepare_file(path):
    print("prepare_file")

class _analyse:
    _instance = None

    _genres = [
        "pop",
        "metal",
        "disco",
        "blues",
        "reggae",
        "classical",
        "rock",
        "hiphop",
        "country",
        "jazz",
    ]

    def predict(self, path):

        # extract the mfccs
        mfcc = self.load_file(path)
        print(mfcc)

        prediction = 'I think it is a potaote'

        return prediction


    def load_file(self, path):
        mfcc = np.array(prepare_file(path))

        return mfcc


#  stops multiple instances running at the same time
def analysis_instance():
    if _analyse._instance is None:
        _analyse._instance = _analyse()
    return _analyse._instance
