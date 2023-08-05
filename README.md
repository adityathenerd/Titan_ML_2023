# A Holistic Approach to Fitness: Team HackSmiths

## Theme: 
Fit Score: Non-Invasive Health Monitoring and Diagnostics Hackathon

## Description:
Fitness watches are a necessity for anyone seeking to optimize their fitness journey. With advanced features like heart rate monitoring, step tracking, and sleep analysis, these watches empower you to take control of your health and achieve your fitness goals more effectively.

## Problem Statement:
• Lack of User-friendly Data
• Ignored aspect of Mental Health Score
• Tracking Menstrual Cycle

## Our Solution:
### Collection of Vitals
We used 3 sensors, MPU6050 (for accelerometer, gyroscope and temperature data), SEN-11574 (Pulse Signal) and MAX30102 (for PPG signal to find Oxygen Saturation). We have used ESP32 (Arduino based) for collecting data and sending over wifi to Firebase (RTDB). 
### Predictive And Calculative Models: 
We have used two models - LSTM Model from Tensorflow (keras) to determine HAR and Random Forest Classifier Model to determine HRV. 
### Representation and Visualisations: 
We developed a Streamlit empowered interactive user interface to show the fitness score, ranging from 0-100, at the frontend. It broadly divided into two sections - Health Fitness and Individual Score Analysis. 

## Set-up:
Run the following code to set-up project in your local system:
```bash
$ git clone https://github.com/adityathenerd/Titan_ML_2023/tree/secondary
$ cd Titan_ML_2023
$ pip install requirements.txt
```
## Usage:
Run the following code to use the streamlit app on your system:
```bash
$ streamlit run demo.py
```

## Deployed Link:
[Click here](https://hacksmiths.streamlit.app/) to check the deployed demo project.

Cheers,
Team HackSmiths.


