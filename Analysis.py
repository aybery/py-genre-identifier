import librosa
import librosa.display

import matplotlib.pyplot as plt
import numpy as np

from constants import (
    UPLOAD_FOLDER,
    SAMPLE_RATE
)


class GetData:
    def __init__(self, file, path):
        self.file = file
        self.path = path
        self.sr = SAMPLE_RATE

    def get_tempo(self, y, sr):
        tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
        return tempo

    def get_spec(self, y):
        D = librosa.stft(y)
        S_dB = librosa.amplitude_to_db(np.abs(D), ref=np.max)
        plt.figure()
        librosa.specshow(S_dB)
        plt.colorbar()

        plt.savefig()

    def run(self):
        #  Generates the file path for the audio file
        self.path = UPLOAD_FOLDER + '\\' + self.file

        #  Loads the file from the designated file path
        y, sr = librosa.load(str(self.path), sr=None)
        #  Trims the silence of the beginning and end of the track
        yt, index = librosa.effects.trim(y)

        #  Calls the tempo function to get the tempo of the audio, value returned is the tempo value
        tempo = self.getTempo(yt, sr)
        #  Gets the duration of the audio file with is stored in a variable
        dur = librosa.get_duration(y=yt, sr=sr)

        return tempo, dur
