import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
import pickle
from scipy import stats

with open('har_pickle', 'rb') as f:
    har = pickle.load(f)

def predict_har(df_50_xyz):
    pred = har.predict(df_50_xyz)
    max_values = np.max(pred, axis=1)
    max_pos = np.argmax(pred, axis=1)

    max_prob = np.array(max_values)
    cat_i = np.array(max_pos)
    cat = []

    for i in range(0, 50, 1):
        cat_a = ['Jogging', 'Walking', 'Upstairs', 'Downstairs', 'Sitting',
        'Standing']
        cat_ = cat_a[cat_i[i]]
        cat.append(cat_)

    return cat

