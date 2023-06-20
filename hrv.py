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
import pickle


with open('hrv_pickle', 'rb') as f:
    predict_stress = pickle.load(f)

def calc_hrv(MEAN_RR, SDRR, RMSSD):
    df = pd.DataFrame({'MEAN_RR':[MEAN_RR],
                   'SDRR': [SDRR],
                   'RMSSD': [RMSSD]
                   })
    cat_i = predict_stress.predict(df)
    cat_i = cat_i[0]
    cat_a = ['no stress', 'interruption', 'time pressure']
    cat = cat_a[cat_i]
    cat_prob = predict_stress.predict_proba(df)[:, cat_i]
    prob_perc = np.mean(cat_prob)*100

    return prob_perc, cat

# print(calc_hrv(898.2928684, 108.1994235, 14.50760903))