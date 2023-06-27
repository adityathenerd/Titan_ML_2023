# imports
import numpy as np
import pandas as pd
from pandas import Series

# datasets
columns = ['user','activity','timestamp', 'x-axis', 'y-axis', 'z-axis']
df_har = pd.read_csv('WISDM_ar_v1.1/WISDM_ar_v1.1_raw.txt', header = None, names = columns, error_bad_lines=False)

# user-19:
user_19_df = df_har[df_har['user'] == 19]

# user-19 activity
user_19_df_jogging = user_19_df[user_19_df['activity'] == 'Jogging'].reset_index(drop=True)
user_19_df_walking = user_19_df[user_19_df['activity'] == 'Walking'].reset_index(drop=True)
user_19_df_upstairs = user_19_df[user_19_df['activity'] == 'Upstairs'].reset_index(drop=True)
user_19_df_downstairs = user_19_df[user_19_df['activity'] == 'Downstairs'].reset_index(drop=True)
user_19_df_sitting = user_19_df[user_19_df['activity'] == 'Sitting'].reset_index(drop=True)
user_19_df_standing = user_19_df[user_19_df['activity'] == 'Standing'].reset_index(drop=True)

sitting_MET = 2
jogging_MET = 7
walking_MET = 3.5
upstairs_MET = 8.3
downstairs_MET = 5
standing_MET = 5

jogging_time = (user_19_df_jogging['timestamp'][len(user_19_df_jogging)-1]-user_19_df_jogging['timestamp'][0])/6000000000
sitting_time = (user_19_df_sitting['timestamp'][len(user_19_df_sitting)-1]-user_19_df_sitting['timestamp'][0])/6000000000
walking_time = (user_19_df_walking['timestamp'][len(user_19_df_walking)-1]-user_19_df_walking['timestamp'][0])/6000000000
upstairs_time = (user_19_df_upstairs['timestamp'][len(user_19_df_upstairs)-1]-user_19_df_upstairs['timestamp'][0])/6000000000
downstairs_time = (user_19_df_downstairs['timestamp'][len(user_19_df_downstairs)-1]-user_19_df_downstairs['timestamp'][0])/6000000000
standing_time = (user_19_df_standing['timestamp'][len(user_19_df_standing)-1]-user_19_df_standing['timestamp'][0])/6000000000

def cal_jogging(weight):
    calories = jogging_time*(jogging_MET*3.5*weight)/200
    return calories

def cal_sitting(weight):
    calories = sitting_time*(sitting_MET*3.5*weight)/200
    return calories

def cal_standing(weight):
    calories = standing_time*(standing_MET*3.5*weight)/200
    return calories

def cal_downstairs(weight):
    calories = downstairs_time*(downstairs_MET*3.5*weight)/200
    return calories

def cal_upstairs(weight):
    calories = upstairs_time*(upstairs_MET*3.5*weight)/200
    return calories

def cal_walking(weight):
    calories = walking_time*(walking_MET*3.5*weight)/200
    return calories

def total_cal(weight):
    calories = (jogging_time*jogging_MET + sitting_time*sitting_MET + standing_MET*standing_time + downstairs_MET*downstairs_time + upstairs_MET*upstairs_time + standing_time*standing_MET)*3.5*weight/200
    return calories

