# imports
from hrvanalysis import get_frequency_domain_features
from hrvanalysis import get_frequency_domain_features
from hrvanalysis import get_sampen
import numpy as np
import pandas as pd
import scipy.stats as sc
from scipy.signal import welch
import antropy as ant
import csv
import heartpy as hp
import matplotlib.pyplot as plt

# import csv file
sample = pd.read_csv('pulse sensor.csv')
#sample = sample.drop(sample.columns[[0, 1, 2, 4, 5]], axis=1)
sample = sample.drop(sample.columns[[0, 1]], axis=1)
sample = sample.drop(sample.columns[[1, 3, 4]], axis=1)
sample = sample.iloc[2:]
sample = sample.reset_index(drop=True)
sample.columns = ['Timestamp', 'pulse']

sample['Timestamp'] = pd.to_datetime(sample['Timestamp'])
sample['Time(sec)'] = (sample['Timestamp']-sample['Timestamp'].iloc[0]).dt.total_seconds()

sample = sample.drop(sample.columns[[0]], axis=1)
sample = sample.iloc[:, ::-1]

# convert the string values to integer
pulse = [int(num) for num in sample['pulse']]
timer = [int(num) for num in sample['Time(sec)']]

# When we have several heartbeats next to each other, 
# then the distance (in milliseconds) between each “R” is defined as the 
# “RR interval” (or sometimes the “NN interval” to emphasize that the heartbeats are normal).

rr_intervals = np.diff(pulse)

# parameters needed for hrv
def mean_rr(nn_intervals):
  mean_rr = np.mean(nn_intervals)
  return mean_rr

def sdrr(nn_intervals):
  diff = np.diff(nn_intervals)
  sdrr = np.sqrt(np.sum(diff**2) / (len(diff) - 1))
  return sdrr

def rmssd(nn_intervals):
  diff = np.diff(nn_intervals)
  rmssd = np.sqrt(np.mean(diff**2))
  return rmssd

# Import these paras to hrv.py to calc hrv
MEAN_RR = mean_rr(rr_intervals)
SDRR = sdrr(rr_intervals)
RMSSD = rmssd(rr_intervals)

print(MEAN_RR)
print(SDRR)
print(RMSSD)