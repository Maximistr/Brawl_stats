packages = {
    "matplotlib": "matplotlib",
    "pandas": "pandas",
    "numpy": "numpy",
    "dotenv": "python-dotenv",
}

for import_name, install_name in packages.items():
    if importlib.util.find_spec(import_name) is None:
        print(f"Installing {install_name}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", install_name])

import os
import requests
import matplotlib.pyplot as plt
import json
import pandas as pd
import numpy as np
import csv
from datetime import date
from dotenv import load_dotenv
import subprocess
import sys
import importlib
import streamlit as st




load_dotenv()

player_tag = "#JRLLR9QU"
API_TOKEN = os.getenv('BS_API_KEY')
URL = f"https://api.brawlstars.com/v1/"

def get_player(tag):
    """Fetch player info from Brawl Stars API"""
    url = f"{URL}players/{tag.replace('#', '%23')}"
    headers = {'Authorization': f'Bearer {API_TOKEN}'}
    response = requests.get(url, headers=headers)
    return response.json()
def save_trophies_to_csv(player_data):
    """Save player's trophies to a CSV file"""
    trophies = player_data.get('trophies', 0)
    with open('trophies.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([date.today(), trophies])
data = get_player(player_tag)

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
st.write("### Power Levels of Brawlers")
plt.show()

