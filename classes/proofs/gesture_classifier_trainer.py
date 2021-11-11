import pandas as pd
import numpy as np
import sklearn
import joblib
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier

from sklearn.metrics import classification_report, confusion_matrix

# Use scikit to create a classifier object using a tutorial
# https://www.springboard.com/blog/ai-machine-learning/beginners-guide-neural-network-in-python-scikit-learn-0-18/
# Once you've made the classifier,  then you can "pickle" it to save the object to a file. (using joblib)
# Then, you can use that classifier in other programs. 
# https://stackoverflow.com/questions/10592605/save-classifier-to-disk-in-scikit-learn#11169797

my_data = pd.read_csv("classes/proofs/training.csv")

data = my_data

print(data)

#targets = ["out1", "out2", "out3"]
targets = ["thumbStatus", "indexStatus", "middleStatus", "ringStatus", "pinkyStatus"]
predictors = ['thumb1x','thumb1y','thumb1z','thumb2x','thumb2y','thumb2z','thumb3x','thumb3y','thumb3z','index1x','index1y','index1z','index2x','index2y','index2z','index3x','index3y','index3z','middle1x','middle1y','middle1z','middle2x','middle2y','middle2z','middle3x','middle3y','middle3z','ring1x','ring1y','ring1z','ring2x','ring2y','ring2z','ring3x','ring3y','ring3z','pinky1x','pinky1y','pinky1z','pinky2x','pinky2y','pinky2z','pinky3x','pinky3y','pinky3z']


x = data[predictors].values
y = data[targets].values

while 1:
    x_train, x_test, y_train, y_test = train_test_split(x,y)

    scaler = StandardScaler()

    scaler.fit(x_train)

    x_train = scaler.transform(x_train)
    x_test = scaler.transform(x_test)

    mlp = MLPClassifier(hidden_layer_sizes=(12,15,5),max_iter=1000)

    mlp.fit(x_train, y_train)

    predictions = mlp.predict(x_test)
    print("Predictions:")
    print(predictions)

    #print(confusion_matrix(y_test, predictions))
    print()
    print(classification_report(y_test,predictions))

    print("Save current model? y/n")
    cont = input(">> ")
    if cont.lower() == "y":
        # pickle and save the object
        joblib.dump(mlp, "gesture_classifier")
        break
    else:
        print("Re-running the trainer...")
