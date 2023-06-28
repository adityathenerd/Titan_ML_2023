import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
import pickle
from scipy import stats

columns = ['user','activity','timestamp', 'x-axis', 'y-axis', 'z-axis']
df_har = pd.read_csv('WISDM_ar_v1.1_raw.txt', header = None, names = columns, error_bad_lines=False)

# user-19:
user_19_df = df_har[df_har['user'] == 19]
df = user_19_df.drop(user_19_df.columns[[0, 1, 2]], axis=1)

n_time_steps = 50
step = 10

segments = []
for i in range (0, df.shape[0]-n_time_steps, step):
    xs = df['x-axis'].values[i: i+50]
    ys = df['y-axis'].values[i: i+50]
    zs = df['z-axis'].values[i: i+50]
    segments.append([xs, ys, zs])

reshaped_segments = np.array(segments).reshape(-1, n_time_steps, 3)

with open('har_pickle', 'rb') as f:
    har = pickle.load(f)

def predict_har(input_tensor):
    pred = har.predict(input_tensor)
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
