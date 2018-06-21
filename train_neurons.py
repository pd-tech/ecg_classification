import os
import sys
import pathlib
from sklearn import preprocessing
from sklearn.neural_network import MLPClassifier
from sklearn.utils import shuffle
from sklearn.externals import joblib
from sklearn.model_selection import KFold

def ecg_reader():
    labels = []
    volts = []
    ecg_data = []

    for csvpath in pathlib.Path("training_data").glob('**/*.csv'):
        parent_dir_name = os.path.split(os.path.dirname(csvpath))[1]

        #print(filepath.absolute())
        if "clean_ecg" in parent_dir_name   : labels.append([1.0,0.0,0.0,0.0,0.0,0.0,0.0])
        if "electrical" in parent_dir_name  : labels.append([0.0,1.0,0.0,0.0,0.0,0.0,0.0])
        if "linear_drift" in parent_dir_name: labels.append([0.0,0.0,1.0,0.0,0.0,0.0,0.0])
        if "sinus_drift" in parent_dir_name : labels.append([0.0,0.0,0.0,1.0,0.0,0.0,0.0])
        if "abrupt" in parent_dir_name      : labels.append([0.0,0.0,0.0,0.0,1.0,0.0,0.0])
        if "square_sig" in parent_dir_name  : labels.append([0.0,0.0,0.0,0.0,0.0,1.0,0.0])
        if "myopotential" in parent_dir_name: labels.append([0.0,0.0,0.0,0.0,0.0,0.0,1.0])

        with open(csvpath, newline='') as csvfile:
            num_samples = 1
            for row in csvfile:
                volts.append(float(row.split(' ')[1]))
                if num_samples >= 2048: break
                num_samples += 1

        ecg_data.append(volts)
        volts = []
        #volts.clear()

    return ecg_data, labels

def main():
    if len(sys.argv) <= 1:
        print("Usage: {0} training_dir=folder".format(sys.argv[0]))

    print("Reading ECG data... Please, wait a minute.\n")
    ecg_data, labels = ecg_reader()
    kf = KFold(n_splits=3)

    print("Preprocessing loaded data...\n")
    ecg_data, labels = shuffle(ecg_data, labels, random_state=0)
    #print(ecg_data[28])
    #ecg_data_scaled = preprocessing.scale(ecg_data)
    
    print("Training neural network... This may take a time.\n")
    #noise_classifier = MLPClassifier(solver='adam', alpha=1e-5, hidden_layer_sizes=(28, 13), shuffle=True, random_state=1)
    noise_classifier = MLPClassifier(solver='adam', alpha=1e-5, hidden_layer_sizes=(28, 13), shuffle=True, random_state=1, activation="tanh", verbose=True, max_iter=2000, early_stopping=False)

    train_data = []
    train_labels = []

    test_data = []
    test_labels = []

    for train_index, test_index in kf.split(ecg_data):
        for train in train_index:
            train_data.append(ecg_data[train])
            train_labels.append(labels[train])
        
        for test in test_index:
            test_data.append(ecg_data[test])
            test_labels.append(labels[test])

    noise_classifier.fit(train_data, train_labels)
    

    print("Saving trained model to disk...")
    joblib.dump(noise_classifier, "noise_classifier.tnm")

    #print(ecg_data[28])
    print("Testing a neural network...\n")
    print("Expected result: " + str(labels[100]))

    print("\n----------------\nClassificated by neural network as: " + str(noise_classifier.predict_proba([ecg_data[100]])))

if __name__ == '__main__':
    main()


