import streamlit as st
import pandas as pd
import random
import time
#from blueTooth import monitor
############### setup webpage #############################
st.set_page_config(
    page_title="Heart Rate Dashboard",
    page_icon="♥️",
    layout="wide",
)
hide_default_format = """
       <style>
       #MainMenu {visibility: hidden; }
       footer {visibility: hidden;}
       </style>
       """
st.markdown(hide_default_format, unsafe_allow_html=True)

###################### finish setup #####################

#Initialize variables
placeholder = st.empty()
heart_rate_trend = []


#Website data
for seconds in range(200):
    
    with placeholder.container():
        bluetooth_data=random.random()*100+60
        heart_rate_trend.append(bluetooth_data)
        #For rolling window
        #if len(heart_rate_trend)>30:
        #    heart_rate_trend.pop(0)


        st.title("Heart rate monitor dashboard")
        st.write(f"your current heart rate is: {int(bluetooth_data)} bpm")

        st.line_chart(heart_rate_trend)
        time.sleep(3)
