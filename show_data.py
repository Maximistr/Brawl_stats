import matplotlib.pyplot as plt
import json
import pandas as pd
import numpy as np
import csv
import streamlit as st

with open('player_data.json', 'r') as file:
    data = json.load(file)

brawlers = pd.DataFrame(data["brawlers"])
tropy_data = pd.read_csv('trophies.csv', names=['Date', 'Trophies'])

figure, axes = plt.subplots(2,2, figsize=(12, 8))

power_levels = brawlers['power'].value_counts()
power_bars = axes[0,0].bar(power_levels.index, power_levels.values, color='purple')
axes[0,0].bar_label(power_bars)
axes[0,0].set_title('Power Levels of Brawlers')
axes[0,0].set_xlabel('Power Level')

axes[0,1].plot(tropy_data['Date'], tropy_data['Trophies'], marker='o', color='yellow')
axes[0,1].set_title('Trophy Progression')
axes[0,1].set_ylabel('Trophies')
st.write("### Trophy Progression Over Time")
st.pyplot(figure)
st.write("### Power Levels of Brawlers")
plt.show()
