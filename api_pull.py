import os
import requests
import json
from datetime import date
from dotenv import load_dotenv
import subprocess
import sys
import csv

load_dotenv()

player_tag = "#JRLLR9QU"
API_TOKEN = os.getenv('BS_API_KEY')
URL = "https://bsproxy.royaleapi.dev/v1/"

def get_player(tag):
    """Fetch player info from Brawl Stars API"""
    url = f"{URL}players/{tag.replace('#', '%23')}"
    headers = {'Authorization': f'Bearer {API_TOKEN}'}
    response = requests.get(url, headers=headers)
    with open('player_data.json', 'w') as file:
        json.dump(response.json(), file, indent=2)
    return response.json()
    
def save_trophies_to_csv(player_data):
    """Save player's trophies to a CSV file"""
    trophies = player_data.get('trophies', 0)
    with open('trophies.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([date.today(), trophies])
        
if __name__ == "__main__":
    player_data =get_player(player_tag)
    save_trophies_to_csv(player_data)
