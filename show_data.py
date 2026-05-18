import plotly.express as px
import json
import pandas as pd
import numpy as np
import csv
import streamlit as st

with open('player_data.json', 'r') as file:
    data = json.load(file)

st.title("Brawl Stars Player Data Visualization")
col1, col2, col3 = st.columns(3)

st.set_page_config(layout="wide")
    
brawlers = pd.DataFrame(data["brawlers"])
tropy_data = pd.read_csv('trophies.csv', names=['Date', 'Trophies'])
elo_data = pd.read_csv('elo.csv', names=['Date', 'ELO'])
hypers_missing = (brawlers['hyperCharges'].str.len() == 0).sum()
gadgets = brawlers["gadgets"].str.len().sum()
starpowers = brawlers["starPowers"].str.len().sum()
power_levels = brawlers['power'].value_counts()
rank_counts = sorted(brawlers['rank'].value_counts().items(), key=lambda x: x[0])
rank_counts = pd.Series({rank: count for rank, count in rank_counts})

power_bars = px.bar(power_levels, x=power_levels.index, y=power_levels.values,
             labels={'x': 'Power Level', 'y': 'Number of Brawlers'},
             title='Distribution of Brawlers by Power Level',
             text=power_levels.values, template='plotly_dark',
             text_auto=False)
power_bars.update_traces(textposition='outside')
power_bars.update_layout(xaxis = dict(tickmode = 'linear',dtick = 1))

tropy_line = px.line(tropy_data, x='Date', y='Trophies',
             labels={'Date': 'Date', 'Trophies': 'Trophies'},
             title='Trophies Over Time',
             template='plotly_dark')
tropy_line.update_traces(line_color="#F6FF00")
tropy_line.update_layout(margin=dict(r=50))

elo_line = px.line(elo_data, x='Date', y='ELO',
             labels={'Date': 'Date', 'ELO': 'ELO'},
             title='Ranked ELO Over Time',
             template='plotly_dark')
elo_line.update_traces(line_color="#006EFF")
elo_line.update_layout(margin=dict(r=50))

def get_rank_label(rank):
    ranks[rank -1] += 1
    if rank == 1:
        return '0-250'
    elif rank == 2:
        return '250-500'
    elif rank == 3:
        return '500-750'
    elif rank == 4:
        return '750-1000'
    elif rank >= 5:
        return f'{1000 * (rank - 4)}-{1000 * (rank - 3)}'
ranks = [0] * rank_counts.index.max()
rank_labels = [get_rank_label(rank) for rank in rank_counts.index]
tier_colors = ["#9a3f2e", "#f67114", "#9895cd", "#faaf0d", "#b26dfd","#f4639a","#f4ed66"]

if len(rank_labels) > len(tier_colors):
    for i in range(len(rank_labels) - len(tier_colors)):
        tier_colors.append("#f4ed66")
for x in range(len(ranks)):
    if ranks[x] == 0:
        tier_colors.remove(tier_colors[x])
rank_pie = px.pie(rank_counts, names=rank_labels, values=rank_counts.values,
             title='Distribution of Brawlers by Rank')
rank_pie.update_traces(marker_colors=tier_colors, textinfo='percent+label', textposition='inside')

with col1:
    st.write("### Power Levels of Brawlers") 
    st.plotly_chart(power_bars,width="stretch")

    st.write("### Ranks of Brawlers")
    st.plotly_chart(rank_pie,width="stretch")

with col2:
    st.write("### Trophies Over Time")
    st.plotly_chart(tropy_line,width="stretch")

    st.write("### Ranked ELO Over Time")
    st.plotly_chart(elo_line,width="stretch")

with col3:
    st.write("### Gadgets, Star Powers, and Hypers")
    with st.container():
        st.markdown(
            f"""
            <div style="display: flex; align-items: center; background-color: #1e1e1e; padding: 15px; border-radius: 10px;">
                <img src="app/static/Images/gadget.webp" style="width: 80px; height: auto; margin-right: 20px;">
                <div>
                    <h4 style="margin: 0; color: white;">Total Gadgets</h4>
                    <p style="margin: 0; font-size: 20px; font-weight: bold; color: #f67114;">{gadgets} / {len(brawlers)}</p>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
