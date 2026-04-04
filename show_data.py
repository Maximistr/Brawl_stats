import plotly.express as px
import json
import pandas as pd
import numpy as np
import csv
import streamlit as st

with open('player_data.json', 'r') as file:
    data = json.load(file)

col1, col2, col3 = st.columns(3)
st.set_page_config(layout="wide")
    
brawlers = pd.DataFrame(data["brawlers"])
tropy_data = pd.read_csv('trophies.csv', names=['Date', 'Trophies'])
power_levels = brawlers['power'].value_counts()
rank_counts = sorted(brawlers['rank'].value_counts().items(), key=lambda x: x[0])
print(rank_counts)
rank_counts = pd.Series({rank: count for rank, count in rank_counts})

power_bars = px.bar(power_levels, x=power_levels.index, y=power_levels.values,
             labels={'x': 'Power Level', 'y': 'Number of Brawlers'},
             title='Distribution of Brawlers by Power Level',
             text=power_levels.values, template='plotly_dark',
             text_auto=False)
power_bars.update_traces(textposition='outside')
power_bars.update_layout(xaxis = dict(tickmode = 'linear',dtick = 1))
def get_rank_label(rank):
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
rank_labels = [get_rank_label(rank) for rank in rank_counts.index]
tier_colors=["#9a3f2e", "#f67114", "#9895cd", "#faaf0d", "#b26dfd","#f4639a","#f4ed66"]
if len(rank_labels) > 7:
    for i in range(len(rank_labels) - 7):
        tier_colors.append("#f4ed66")

tropy_line = px.line(tropy_data, x='Date', y='Trophies',
             labels={'Date': 'Date', 'Trophies': 'Trophies'},
             title='Trophies Over Time',
             template='plotly_dark')
tropy_line.update_traces(line_color="#F6FF00")
tropy_line.update_layout(
    xaxis = dict(
        dtick = 86400000,
        tickformat = '%b %e'
    )
)

rank_pie = px.pie(rank_counts, names=rank_labels, values=rank_counts.values,
             title='Distribution of Brawlers by Rank')
rank_pie.update_traces(marker_colors=tier_colors, textinfo='percent+label', textposition='inside')

with col1:
    st.write("### Power Levels of Brawlers") 
    st.plotly_chart(power_bars,width="stretch")

with col2:
    st.write("### Trophies Over Time")
    st.plotly_chart(tropy_line,width="stretch")

with col3:
    st.write("### Ranks of Brawlers")
    st.plotly_chart(rank_pie,width="stretch")
    
