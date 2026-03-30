import plotly.express as px
import json
import pandas as pd
import numpy as np
import csv
import streamlit as st

with open('player_data.json', 'r') as file:
    data = json.load(file)
    
col1, col2 = st.columns(2)
    
brawlers = pd.DataFrame(data["brawlers"])
tropy_data = pd.read_csv('trophies.csv', names=['Date', 'Trophies'])
power_levels = brawlers['power'].value_counts()

power_bars = px.bar(power_levels, x=power_levels.index, y=power_levels.values,
             labels={'x': 'Power Level', 'y': 'Number of Brawlers'},
             title='Distribution of Brawlers by Power Level',
             text=power_levels.values, template='plotly_dark',
             color=power_levels.index, text_auto=False)
power_bars.update_traces(textposition='outside')

tropy_line = px.line(tropy_data, x='Date', y='Trophies',
             labels={'Date': 'Date', 'Trophies': 'Trophies'},
             title='Trophies Over Time',
             template='plotly_dark')

with col1:
    st.write("### Distribution of Brawlers by Power Level") 
    st.plotly_chart(power_bars, use_container_width=True)

with col2:
    st.write("### Trophies Over Time")
    st.plotly_chart(tropy_line, use_container_width=True)

