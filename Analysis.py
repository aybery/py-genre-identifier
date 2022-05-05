import librosa
import random

import matplotlib.pyplot as plt
import numpy as np

from constants import (
    UPLOAD_FOLDER,
    TEST_DATA,
    SAMPLE_RATE
)


class GetData:
    def __init__(self, file, path):
        self.file = file
        self.path = path
        self.sr = SAMPLE_RATE

    def getTempo(self, y, sr):
        tempo, beat_frames = librosa.beat.beat_track(y, sr=sr)
        return tempo

    def getSpec(self, y, sr):
        window_size = 1024
        window = np.hanning(window_size)
        stft = librosa.core.spectrum.stft(y, n_fft=window_size, hop_length=512, window=window)
        out = 2 * np.abs(stft) / np.sum(window)

        # For plotting headlessly
        from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

        fig = plt.Figure()
        canvas = FigureCanvas(fig)
        ax = fig.add_subplot(111)
        p = librosa.display.specshow(librosa.amplitude_to_db(out, ref=np.max), ax=ax, y_axis='log', x_axis='time')

        fig.savefig('static/img/specta.png')
        #print(fig.savefig('spec.png'))


    def run(self):
        self.path = UPLOAD_FOLDER + '\\' + self.file
        print(self.path)
        y, sr = librosa.load(str(self.path), sr=None)
        tempo = self.getTempo(y, sr)
        dur = librosa.get_duration(y=y, sr=sr)
        return tempo, dur
