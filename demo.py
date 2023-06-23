import streamlit as st
import pandas as pd
import numpy as np
from hrv import *

navigation_sidebar = st.sidebar.selectbox('Choose an option',('Health Fitness Score', 'Individual Score Analysis'))

st.header("Applicant's Details")


print(calc_hrv(898.2928684, 108.1994235, 14.50760903))

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

