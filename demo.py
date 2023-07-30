import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from hrv import *
from pulse_analysis import *
from calorie_counter import *

################fitness score ##############
##### pulse 
real_pulse = 80
avg_pulse = 92
# real_pulse/avg_pulse*30*(factor)
v_pulse = (80/92)*30*0.75

####### stress cat
# v_stress = 20 - (percentage of type of stress)*(weightage of that stress)
v_stress = 20
percent, category =  pred_hrv(MEAN_RR,SDRR,RMSSD)
if category == 'time pressure':
    v_stress = 20 - (percent/100)*16
if category == 'interruption':
    v_stress = 20 - (percent/100)*8

###### calories burnt
def BMR_men(weight, height, age):
    # Men: BMR = 88.362 + (13.397 x weight in kg) + (4.799 x height in cm) – (5.677 x age in years)
    BMR = 88.362 + (13.397*weight) + (4.799*height) - (5.677*age)
    return BMR

def BMR_women(weight, height, age):
    # Women: BMR = 447.593 + (9.247 x weight in kg) + (3.098 x height in cm) – (4.330 x age in years)
    BMR = 447.593 + (9.2478*weight) + (3.098*height) - (4.330*age)
    return BMR

## calorie counter
# frac = calorie to be burnt - calorie burnt / calorie to be burnt
# v_calorie = (1-frac) * 25
frac = (BMR_men(65,170,21) - total_cal(65))/BMR_men(65,170,21)
if frac < 0:
    frac = 0
v_calorie = (1-frac)*25

#v_sleep = no of hours slept/8*(sleep weightage)*(factor)
v_sleep = 6.5/8*10*0.85
#if val >= 98 and val <= 100 no change in v_spo2 else v_spo2 = (val/98) * (factor)
v_spo2 = 12.5*0.75

fitness_score = v_pulse+v_stress + v_calorie + v_sleep + v_spo2
# print(v_pulse)
# print(v_stress)
# print(v_calorie)
# print(v_sleep)
# print(v_spo2)


############################################

#sidebar
navigation_sidebar = st.sidebar.selectbox('Choose an option',('Health Fitness Score', 'Individual Score Analysis'))
#calling HRV


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
    st.markdown("_The following details are included regarding the inputs:_")
    st.markdown("**Pulse:** _The pulse was measured within a duration of 125 seconds, providing a comprehensive assessment of the user's heart rate._")
    st.markdown("**Activity Tracker:** _The activity tracker encompasses various physical activities, including jogging, walking, going upstairs, going downstairs, sitting, and standing. This allows for accurate tracking and monitoring of the user's daily movement patterns._")
    st.markdown("**BMI (Body Mass Index):** _BMI is a crucial measure for evaluating general health and is calculated based on the user's height and weight ratio. It provides valuable insights into the user's body composition and overall health status._")
    input_box = st.selectbox('Input', ('Pulse Rate', 'Activity Tracker', 'BMI Metrics'))

    if input_box == 'Pulse Rate':
        pulse_rate_fig = px.line(sample, x = "Time(sec)", y = "pulse",title="Pulse Rate")
        pulse_rate_fig.update_traces(line_color = "red")
        st.plotly_chart(pulse_rate_fig)

    if input_box == 'BMI Metrics':
        weight = st.number_input("Enter weight (in kg)", min_value=0.0, max_value=200.0, step=0.5)
        height = st.number_input("Enter height (in m)", min_value=0.01, max_value=2.5, step = 0.01)
        bmi = weight/(height*height)
        if st.button("Check BMI") and weight > 0 and height > 0 :
            st.write(bmi)

    if input_box == 'Activity Tracker':
        #########################################Jogging
        # plot 1 
        x1 = tuple(range(0,501))
        y1 = user_19_df_jogging['x-axis'][:501]

        #plot 2
        x2 = tuple(range(0,501))
        y2 = user_19_df_jogging['y-axis'][:501]

        #  plot 3
        x3 = tuple(range(0,501))
        y3 = user_19_df_jogging['z-axis'][:501]

        st.title("Activities")
        st.subheader("Jogging")
        fig, axs = plt.subplots(1, 3, figsize=(15, 4))

        axs[0].plot(x1, y1)
        axs[0].set_title("X-axis")
        
        axs[1].plot(x2, y2)
        axs[1].set_title("Y-axis")
        
        axs[2].plot(x3, y3)
        axs[2].set_title("z-axis")
        fig.tight_layout()

        st.pyplot(fig)

        ##############################  Walking
         # plot 1 
        x1 = tuple(range(0,501))
        y1 = user_19_df_walking['x-axis'][:501]

        #plot 2
        x2 = tuple(range(0,501))
        y2 = user_19_df_walking['y-axis'][:501]

        #  plot 3
        x3 = tuple(range(0,501))
        y3 = user_19_df_walking['z-axis'][:501]

        st.subheader("Walking")
        fig, axs = plt.subplots(1, 3, figsize=(15, 4))

        axs[0].plot(x1, y1)
        axs[0].set_title("X-axis")
        
        axs[1].plot(x2, y2)
        axs[1].set_title("Y-axis")
        
        axs[2].plot(x3, y3)
        axs[2].set_title("z-axis")
        fig.tight_layout()
        
        st.pyplot(fig)

         ############################## Upstairs
         # plot 1 
        x1 = tuple(range(0,501))
        y1 = user_19_df_upstairs['x-axis'][:501]

        #plot 2
        x2 = tuple(range(0,501))
        y2 = user_19_df_upstairs['y-axis'][:501]

        #  plot 3
        x3 = tuple(range(0,501))
        y3 = user_19_df_upstairs['z-axis'][:501]

        st.subheader("Upstairs")
        fig, axs = plt.subplots(1, 3, figsize=(15, 4))

        axs[0].plot(x1, y1)
        axs[0].set_title("X-axis")
        
        axs[1].plot(x2, y2)
        axs[1].set_title("Y-axis")
        
        axs[2].plot(x3, y3)
        axs[2].set_title("z-axis")
        fig.tight_layout()
        
        st.pyplot(fig)

        ############################## Downstairs
        # plot 1 
        x1 = tuple(range(0,501))
        y1 = user_19_df_downstairs['x-axis'][:501]

        #plot 2
        x2 = tuple(range(0,501))
        y2 = user_19_df_downstairs['y-axis'][:501]

        #  plot 3
        x3 = tuple(range(0,501))
        y3 = user_19_df_downstairs['z-axis'][:501]

        st.subheader("Downstairs")
        fig, axs = plt.subplots(1, 3, figsize=(15, 4))

        axs[0].plot(x1, y1)
        axs[0].set_title("X-axis")
        
        axs[1].plot(x2, y2)
        axs[1].set_title("Y-axis")
        
        axs[2].plot(x3, y3)
        axs[2].set_title("z-axis")
        fig.tight_layout()
        
        st.pyplot(fig)

        
        ############################## Standing
        # plot 1 
        x1 = tuple(range(0,501))
        y1 = user_19_df_standing['x-axis'][:501]

        #plot 2
        x2 = tuple(range(0,501))
        y2 = user_19_df_standing['y-axis'][:501]

        #  plot 3
        x3 = tuple(range(0,501))
        y3 = user_19_df_standing['z-axis'][:501]

        st.subheader("Standing")
        fig, axs = plt.subplots(1, 3, figsize=(15, 4))

        axs[0].plot(x1, y1)
        axs[0].set_title("X-axis")
        
        axs[1].plot(x2, y2)
        axs[1].set_title("Y-axis")
        
        axs[2].plot(x3, y3)
        axs[2].set_title("z-axis")
        fig.tight_layout()
        
        st.pyplot(fig)

        ############################## Sitting
        # plot 1 
        x1 = tuple(range(0,501))
        y1 = user_19_df_sitting['x-axis'][:501]

        #plot 2
        x2 = tuple(range(0,501))
        y2 = user_19_df_sitting['y-axis'][:501]

        #  plot 3
        x3 = tuple(range(0,501))
        y3 = user_19_df_sitting['z-axis'][:501]

        st.subheader("Sitting")
        fig, axs = plt.subplots(1, 3, figsize=(15, 4))

        axs[0].plot(x1, y1)
        axs[0].set_title("X-axis")
        
        axs[1].plot(x2, y2)
        axs[1].set_title("Y-axis")
        
        axs[2].plot(x3, y3)
        axs[2].set_title("z-axis")
        fig.tight_layout()
        
        st.pyplot(fig)

        







############
# individual score analysis
if navigation_sidebar == 'Individual Score Analysis':

    st.header("Overall Fitness Score")
    st.write("*Fitness score calculatd here is taken for a user weighing 65 kgs with the activity and pulse rate shown in the input section before.*")
    fitness_score = round(fitness_score, 2)
    health_header = ""
    if fitness_score <=40:
        st.markdown(f'<h2 style="color: red;">{fitness_score}</h2>', unsafe_allow_html=True)
        health_header ="Keep pushing yourself! There's room for improvement, but with dedication, you'll reach your fitness goals."
        st.markdown(f'<h6 style="color: red;">{health_header}</h6>', unsafe_allow_html=True)
         
    if fitness_score >40 and fitness_score <=60:
        st.markdown(f'<h2 style="color: orange;">{fitness_score}</h2>', unsafe_allow_html=True)
        health_header ="You're on the right track! Stay consistent and focused, and you'll see progress in no time."
        st.markdown(f'<h6 style="color: orange;">{health_header}</h6>', unsafe_allow_html=True)

    if fitness_score >60 and fitness_score <=80:
        st.markdown(f'<h2 style="color: #50C878;">{fitness_score}</h2>', unsafe_allow_html=True)
        health_header ="Great work! You've made significant strides in your fitness journey. Keep up the momentum and continue challenging yourself."
        st.markdown(f'<h6 style="color:#50C878 ;">{health_header}</h6>', unsafe_allow_html=True)

    if fitness_score >80 and fitness_score <=100:
        st.markdown(f'<h2 style="color: green;">{fitness_score}</h2>', unsafe_allow_html=True)
        health_header ="Wow! You're crushing it! Your dedication and hard work are paying off. Keep up the amazing effort!"
        st.markdown(f'<h6 style="color:  green ;">{health_header}</h6>', unsafe_allow_html=True)

    input_box = st.selectbox('Output', ('Pulse Rate Metrics','Calorie Count Metrics'))
    
    

    if input_box == 'Pulse Rate Metrics':
        result_hrv = pred_hrv(MEAN_RR,SDRR,RMSSD)
        st.write("_Mean RR Interval :_", MEAN_RR )
        st.write("_Root-mean-squared :_",round(RMSSD,3))
        st.write("_Standard-deviation:_",round(SDRR,3))
        v1,v2 = result_hrv
        # pie chart
        hrv_labels = ['Yes', 'No']
        hrv_values = [int(v1), 100-int(v1)]
        ###########
        st.markdown("<span style='color:red'>*</span><span style='color:red'>*</span>", unsafe_allow_html=True)
        st.markdown("**No Stress:** _Participants were allowed to work on tasks for as long as they needed, with a maximum duration of 45 minutes. However, they were unaware of this time limit._")
        st.markdown("**Time pressure:** _Participants faced a reduced time constraint, with the task completion time shortened to 2/3 of the time taken in the neutral condition._")
        st.markdown("**Interruption:** _Participants were interrupted during their assigned tasks._")
        st.header("Probability of " + result_hrv[1])
        fig = go.Figure(data=[go.Pie(labels=hrv_labels, values=hrv_values, pull=[0.05,0])])
        fig.update_traces(marker=dict(colors=['#99ff99', '#66b3ff']))
        st.plotly_chart(fig)


    if input_box == 'Calorie Count Metrics':
        weight = st.number_input("Enter weight (in kg)", min_value=0.0, max_value=200.0, step=0.5)
        if st.button('Submit'):
            lith_dict = {'LITH': ['Sitting', 'Standing', 
                        'Walking', 'Upstairs', 
                        'Downstairs', 'Jogging'],
                'COUNT': [cal_sitting(weight),cal_standing(weight), cal_walking(weight), cal_upstairs(weight), 
                                cal_downstairs(weight), cal_jogging(weight)]}

            df = pd.DataFrame.from_dict(lith_dict)

            # Get key properties for colours and labels
            max_value_full_ring = max(df['COUNT'])

            ring_colours = ['#2f4b7c', '#665191', '#a05195','#d45087',
                        '#f95d6a','#ff7c43']

            ring_labels = [f'   {x} ({v}) ' for x, v in zip(list(df['LITH']), 
                                                            list(df['COUNT']))]
            data_len = len(df)

            # Begin creating the figure
            fig = plt.figure(figsize=(10,10), linewidth=10
                            )

            rect = [0.1,0.1,0.8,0.8]

            # Add axis for radial backgrounds
            ax_polar_bg = fig.add_axes(rect, polar=True, frameon=False)
            ax_polar_bg.set_theta_zero_location('N')
            ax_polar_bg.set_theta_direction(1)

            # Loop through each entry in the dataframe and plot a grey
            # ring to create the background for each one
            for i in range(data_len):
                ax_polar_bg.barh(i, round(max_value_full_ring*1.5*np.pi/max_value_full_ring,2), 
                                color='grey', 
                                alpha=0.1)
            # Hide all axis items
            ax_polar_bg.axis('off')
                
            # Add axis for radial chart for each entry in the dataframe
            ax_polar = fig.add_axes(rect, polar=True, frameon=False)
            ax_polar.set_theta_zero_location('N')
            ax_polar.set_theta_direction(1)
            ax_polar.set_rgrids([0, 1, 2, 3, 4, 5], 
                                labels=ring_labels, 
                                angle=0, 
                                fontsize=14, fontweight='bold',
                                color='black', verticalalignment='center')

            # Loop through each entry in the dataframe and create a coloured 
            # ring for each entry
            for i in range(data_len):
                ax_polar.barh(i, round(list(df['COUNT'])[i]*1.5*np.pi/max_value_full_ring,2), 
                            color=ring_colours[i])


            # Hide all grid elements for the    
            ax_polar.grid(False)
            ax_polar.tick_params(axis='both', left=False, bottom=False, 
                            labelbottom=False, labelleft=True)
            st.set_option('deprecation.showPyplotGlobalUse', False)
            st.pyplot()




