import numpy as np
import pandas as pd
from pandas import Series
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
import seaborn as sns
from sklearn import preprocessing
from sklearn.metrics import classification_report
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import pickle
 

with open('hrv_pickle', 'rb') as f:
    predict_stress = pickle.load(f)

def pred_hrv(MEAN_RR, SDRR, RMSSD):
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

def calculate_hrv(pulse_rate_data):
    # Calculate the RR intervals from the pulse rate data
    rr_intervals = [60 / rate for rate in pulse_rate_data]

    # Calculate the HRV as the standard deviation of RR intervals
    hrv = np.std(rr_intervals)

    return hrv

def calculate_hrv_from_ppg(ppg_signal, sampling_rate):
    # Find the peaks in the PPG signal
    peaks, _ = find_peaks(ppg_signal, height=0.5)  # Adjust the height threshold as needed

    # Calculate the RR intervals from the PPG signal (in seconds)
    rr_intervals = np.diff(peaks) / sampling_rate

    # Calculate the HRV as the standard deviation of RR intervals
    hrv = np.std(rr_intervals)

    return hrv
