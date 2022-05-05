# import matplotlib.pyplot as plt
import numpy as np

import librosa
import csv

from librosa.feature import mfcc

from constants import (
    TEST_DATA,
    SAMPLE_RATE
)


def analyse_file():
    wav = librosa.load()


class Predict:
    def __init__(self, file, path):
        self.filename = file
        self.path = path
        self.prediction = None
        self.dataset = []
        self.sr = SAMPLE_RATE

    def loadDataset(self, file):
        with open(TEST_DATA, 'rb') as f:
            while True:
                try:
                    self.dataset.append(load(f))
                except EOFError:
                    f.close()
                    break

    loadDataset(TEST_DATA)

    def distance(self, instance1, instance2, k):
        distance = 0
        mm1 = instance1[0]
        cm1 = instance1[1]
        mm2 = instance2[0]
        cm2 = instance2[1]
        distance = np.trace(np.dot(np.linalg.inv(cm2), cm1))
        distance += (np.dot(np.dot((mm2 - mm1).transpose(), np.linalg.inv(cm2)), mm2 - mm1))
        distance += np.log(np.linalg.det(cm2)) - np.log(np.linalg.det(cm1))
        distance -= k
        return distance

    def getNeighbors(trainingSet, instance, k):
        distances = []
        for x in range(len(trainingSet)):
            dist = distance(trainingSet[x], instance, k) + self.distance(instance, trainingSet[x], k)
            distances.append((trainingSet[x][2], dist))
        distances.sort(key=operator.itemgetter(1))
        neighbors = []
        for x in range(k):
            neighbors.append(distances[x][0])
        return neighbors

    def nearestClass(neighbors):
        classVote = {}
        for x in range(len(neighbors)):
            response = neighbors[x]
            if response in classVote:
                classVote[response] += 1
            else:
                classVote[response] = 1
        sorter = sorted(classVote.items(), key=operator.itemgetter(1), reverse=True)
        return sorter[0][0]

    def run(self):
        (rate, sig) = librosa.read(self.path)
        mfcc_feat = mfcc(sig, rate, winlen=0.020, appendEnergy=False)
        covariance = np.cov(np.matrix.transpose(mfcc_feat))
        mean_matrix = mfcc_feat.mean(0)
        feature = (mean_matrix, covariance, 0)
        pred = self.nearestClass(self.getNeighbors(self.dataset, feature, 5))
        #  tempo = librosa.helpFINISHTHIS
        y, self.sr = librosa.load(self.path)
        tempo, _ = librosa.beat.beat_track(y, sr=self.sr)

        return pred, tempo
