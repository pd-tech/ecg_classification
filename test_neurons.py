import os
import sys
import pathlib
from sklearn.neural_network import MLPClassifier
from sklearn.externals import joblib
import matplotlib.pyplot as plt
from sklearn import preprocessing

noiseDB = ['Clean', '50Hz', 'Linear', 'Sinus', 'Abrupt', 'Square', 'Myo']

def ecg_reader(csvpath):
    volts = []
    ecg_data = []

    with open(csvpath, newline='') as csvfile:
        num_samples = 1
        for row in csvfile:
            volts.append(float(row.split(' ')[1]))
            if num_samples >= 2048: break
            num_samples += 1

        ecg_data.append(volts)
        volts = []
        #volts.clear()

    return ecg_data

def main():
    if len(sys.argv) <= 1:
        print("Usage: {0} [CSV file for classification]".format(sys.argv[0]))
        return

    print("Reading ECG data... Please, wait a minute.\n")
    ecg_data = ecg_reader(sys.argv[1])

    print("Loading pre-trained model from disk...\n")
    noise_classifier = joblib.load("noise_classifier.tnm")

    #print(ecg_data[28])
    print("Classificating by neural network...\n-----------------------------------")

    resultID = noise_classifier.predict_proba(ecg_data)*100
    fig, ax = plt.subplots()
    ax.bar(noiseDB,resultID[0,:])
    plt.show()
    print(resultID)
    

if __name__ == '__main__':
    main()


