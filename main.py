import pandas as pd
from pbpData import getPBPdata
import os.path

# Pitch-by-pitch (pbp) data for specific year

year = 2021

if os.path.exists('pbpData-' + str(year) + '.csv'):
    print("Data already downloaded!")
    pbp = pd.read_csv('pbpData-' + str(year) + '.csv')
else:
    pbp = getPBPdata(year)



pbp = pd.read_csv('pbpData-' + str(year) + '.csv')

pbp.sort_values(['pitcher', 'game_date'])

    # Total pitch data from Statcast for 2022 -> Used for player id
data = pd.read_csv('totalPitchData' + str(year) + '.csv')

    # Get player id and corresponding name
player_id = data[['player_id', 'player_name']]

    # Adding pitcher names to data frame
pbp = pd.merge(pbp, player_id, left_on="pitcher", right_on="player_id")

    # Remove Spring Training games 
pbp = pbp[pbp['game_type']!= "S"]

#pbp.to_csv('pbp.csv')
print(sum(data["total_pitches"]))
print(len(pbp))

print(data)
