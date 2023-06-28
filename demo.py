import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from hrv import *
from pulse_analysis import *
from calorie_counter import *

#sidebar
navigation_sidebar = st.sidebar.selectbox('Choose an option',('Health Fitness Score', 'Individual Score Analysis'))
#calling HRV
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

    input_box = st.selectbox('Input', ('Pulse Rate', 'Steps Count', 'BMI metrics'))

    if input_box == 'Pulse Rate':
        pulse_rate_fig = px.line(sample, x = "Time(sec)", y = "pulse",title="Pulse Rate")
        pulse_rate_fig.update_traces(line_color = "red")
        st.plotly_chart(pulse_rate_fig)

    if input_box == 'BMI metrics':
        weight = st.number_input("Enter weight (in kg)", min_value=0.0, max_value=200.0, step=0.5)
        height = st.number_input("Enter height (in m)", min_value=0.01, max_value=2.5, step = 0.01)
        bmi = weight/(height*height)
        if st.button("Check BMI") and weight > 0 and height > 0 :
            st.write(bmi)

    if input_box == 'Steps Count':
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
    input_box = st.selectbox('Output', ('Pulse Rate Metrics','Calorie Count Metrics'))
    
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




