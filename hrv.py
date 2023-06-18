# imports
import numpy as np
import pandas as pd
from pandas import Series
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn import preprocessing
from sklearn.metrics import classification_report
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
# import parameters from ppg_analysis.py
from ppg_analysis import MEAN_RR
from ppg_analysis import SDRR
from ppg_analysis import RMSSD

# training and testing data
train = pd.read_csv("train.csv")
test = pd.read_csv("test.csv")

# label encoding
LE = preprocessing.LabelEncoder()
LE.fit(train['condition'])
list(LE.classes_)

train['condition'] = LE.transform(train['condition'])
test['condition'] = LE.transform(test['condition'])

subCols1 = ['MEAN_RR', 'SDRR', 'RMSSD']
subCols2 = subCols1 + ['condition']
train2 = train[subCols2]

# training and testing data split
(X_train, X_test, y_train, y_test) = train_test_split(train[subCols1], train['condition'], test_size = 0.2)

# training data
X_train = train[subCols1]
y_train = train['condition']

# testing data
X_test = test[subCols1]
y_test = test['condition']

# initialising classifier
model = RandomForestClassifier()
model.fit(X_train,y_train)
y_pred = model.predict(X_test)

# function for predicting stress type
def predict_stress(MEAN_RR, SDRR, RMSSD):
    df = pd.DataFrame({'MEAN_RR':[MEAN_RR],
                   'SDRR': [SDRR],
                   'RMSSD': [RMSSD]
                   })
    cat_i = model.predict(df)
    cat_i = cat_i[0]
    cat_a = ['no stress', 'interruption', 'time pressure']
    cat = cat_a[cat_i]
    cat_prob = model.predict_proba(df)[:, cat_i]
    prob_perc = np.mean(cat_prob)*100

    return cat, prob_perc 

predict_stress(MEAN_RR, SDRR, RMSSD)