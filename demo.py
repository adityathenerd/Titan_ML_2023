import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from hrv import *
from pulse_analysis import *
from calorie_counter import *

######
#csv files

navigation_sidebar = st.sidebar.selectbox('Choose an option',('Health Fitness Score', 'Individual Score Analysis'))

calc_hrv(MEAN_RR,SDRR,RMSSD)

if navigation_sidebar == 'Health Fitness Score':
    st.header("Applicant's Details")

    #Applicant's Details
    first_name, last_name = st.columns(2)

    with first_name:
        st.text_input("First Name")
    with last_name:
        st.text_input("Last Name")

    gender, age , dob = st.columns([2,2,4])

    with gender:
        st.selectbox('Gender',('Gender','Male','Female','Others'))
    with age:
        st.selectbox('Age', tuple(range(0,101)))
    with dob:
        st.date_input("YYYY/MM/DD")

    email_id, mobile_no = st.columns([1.5,1])

    with email_id:
        st.text_input('Email Address')
    with mobile_no:
        st.text_input("Mobile Number")

    #Health Details
    st.header("Applicant's Health Details")

    input_box = st.selectbox('Input', ('Pulse Rate', 'Steps Count'))

    if input_box == 'Pulse Rate':
        uploaded_pulse_rate = st.file_uploader("Choose a CSV file",type="csv")
        if uploaded_pulse_rate is None:
            st.write("")
        else:
            pulse_rate_fig = px.line(sample, x = "Time(sec)", y = "pulse",title="Pulse Rate")
            pulse_rate_fig.update_traces(line_color = "red")
            st.plotly_chart(pulse_rate_fig)

# individual score analysis
if navigation_sidebar == 'Individual Score Analysis':
    input_box = st.selectbox('Output', ('Pulse Rate Metrics', 'Calorie Count Metrics'))
    
    if input_box == 'Pulse Rate Metrics':
        result_hrv = calc_hrv(MEAN_RR,SDRR,RMSSD)
        st.write("_Mean RR Interval :_", MEAN_RR )
        st.write("_Root-mean-squared :_",round(RMSSD,3))
        st.write("_Standard-deviation:_",round(SDRR,3))
        v1,v2 = result_hrv
        # pie chart
        hrv_labels = ['Yes', 'No']
        hrv_values = [int(v1), 100-int(v1)]
        ###########
        st.header("Probability of " + result_hrv[1])
        fig = go.Figure(data=[go.Pie(labels=hrv_labels, values=hrv_values, pull=[0.05,0])])
        fig.update_traces(marker=dict(colors=['#99ff99', '#66b3ff']))
        st.plotly_chart(fig)