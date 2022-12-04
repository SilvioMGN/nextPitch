
import pandas as pd
import numpy as np
from pbpData import getPBPdata
from hiddenMarkov import *
import os.path


# Pitch-by-pitch (pbp) data for specific year

year = 2020
'''
if os.path.exists('pbpData-' + str(year) + '.csv'):
    print("Data already downloaded!")
    pbp = pd.read_csv('pbpData-' + str(year) + '.csv')
else:
    pbp = getPBPdata(year)
'''

pbp = pd.read_csv('pbpData-' + str(year) + '.csv')

pbp.sort_values(['pitcher', 'game_date', 'inning'],
                ascending=[True, True, True], inplace=True)

# Total pitch data from Statcast for 2022 -> Used for player id
data = pd.read_csv('totalPitchData' + str(year) + '.csv')

# Get player id and corresponding name
player_id = data[['player_id', 'player_name']]

# Adding pitcher names to data frame
pbp = pd.merge(pbp, player_id, left_on="pitcher", right_on="player_id")

# Remove Spring Training games
pbp = pbp[pbp['game_type'] != "S"]

# pbp.to_csv('pbp.csv')

# print(pbp['pitch_number'])

# only needs to be run if run first time
# TO-DO: Find a better way to do this because it is very time consuming
#newPbp = addTotalPitch(pbp)
#newPbp.to_csv('newPbp.csv')

# TO-DO: Change functiom so that we enter all pitchers here, so the functions gets called for every pitcher seperatly => makes it easier when looking at single pitchers
pitcher = 'Cole, Gerrit'
allPitcherPercentages = transitionProbabilities(pbp, pitcher)
np.save("allPitcherPercentages.npy", allPitcherPercentages)

# allPitcherPercentages = np.load('allPitcherPercentages.npy', allow_pickle=True)
#emission = emissionProbabilities(pbp)
#print(emission)


