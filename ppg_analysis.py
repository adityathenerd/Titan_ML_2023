from hrvanalysis import get_frequency_domain_features
from hrvanalysis import get_frequency_domain_features
from hrvanalysis import get_sampen
import numpy as np
import scipy.stats as sc
from scipy.signal import welch
import antropy as ant
import csv
import heartpy as hp
import matplotlib.pyplot as plt

# When we have several heartbeats next to each other, 
# then the distance (in milliseconds) between each “R” is defined as the 
# “RR interval” (or sometimes the “NN interval” to emphasize that the heartbeats are normal).

bpm = []
nn_intervals = []

# replace the 'sample.csv' with the raw signal csv file
with open(r'sample.csv', 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    
    for row in csvreader:
        bpm.append(float(row[0]))
        nn_intervals.append(float(row[1]))

    for i in range(0,len(bpm)):
        print(bpm[i])

    for i in range(0,len(bpm)):
        print(nn_intervals[i])

frequency_domain_features = get_frequency_domain_features(nn_intervals)
sampen_n = get_sampen(nn_intervals)

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

# Calculate BPM
def get_bpm(data):
   wd, m = hp.process(data, sample_rate=100)
   bpm = m['bpm']
   return bpm

MEAN_RR = mean_rr(nn_intervals)
SDRR = sdrr(nn_intervals)
RMSSD = rmssd(nn_intervals)