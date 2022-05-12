import librosa
import librosa.display
import random

import matplotlib.pyplot as plt
import numpy as np

from constants import (
    MEL_SPEC_LOCATION
)

#  GetData class
class GetData:
    def __init__(self, file, path):
        #  Declares self.variables that can be used
        self.file = file
        self.path = path
        self.y = None
        self.yt = None
        self.sr = None

    #  loads the file into librosa and extracts features
    def run(self):
        self.y, self.sr = librosa.load(str(self.path), sr=None)
        #  Trims the silence of the beginning and end of the track
        self.yt, index = librosa.effects.trim(self.y)

        #  Calls the tempo function to get the tempo of the audio, value returned is the tempo value
        tempo = self.get_tempo()

        #  Gets the duration of the audio file with is stored in a variable
        dur = librosa.get_duration(y=self.yt, sr=self.sr)

        return tempo, dur

    #  Extracts the tempo
    def get_tempo(self):
        #  Gets the tempo of the trimmed track to ensure accuracy
        tempo, beat_frames = librosa.beat.beat_track(y=self.yt, sr=self.sr)
        return tempo

    #  Gets the spectrogram image of the audio file
    def get_spec(self, y):
        #  This does not work
        D = librosa.stft(y)
        S_dB = librosa.amplitude_to_db(np.abs(D), ref=np.max)
        plt.figure()
        librosa.specshow(S_dB)
        plt.colorbar()

        plt.savefig()

    def get_spec_test(self):
        #  This was testing if the image would be created
        x = [1, 2, 3, 4, 5, 6, 7]
        y = []

        for i in range(0, 7):
            val = random.randint(1, 20)
            y.append(val)

        plt.plot(x, y)
        plt.xlabel('X Var')
        plt.ylabel('Y Var')

        plt.savefig(MEL_SPEC_LOCATION)
        print("hi this is me working")
        plt.close()

