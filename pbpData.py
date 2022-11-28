# TO-DO: Change from subprocess to rpy2 for easier handeling of R functions

import subprocess
import pandas as pd

def getPBPdata(year):

    subprocess.run("Rscript scrapePBP.R " + str(year), shell=True)

    filePbp = 'pbpData-' + str(year) + '.csv'

    pbp = pd.read_csv(filePbp)

    pbp.sort_values(['pitcher', 'game_date'])

    # Total pitch data from Statcast for 2022 -> Used for player id
    data = pd.read_csv('totalPitchData' + str(year) + '.csv')

    # Get player id and corresponding name
    player_id = data[['player_id', 'player_name']]

    # Adding pitcher names to data frame
    pbp = pd.merge(pbp, player_id, left_on="pitcher", right_on="player_id")

    # Remove Spring Training games 
    pbp = pbp[pbp['game_type']!= "S"]

    return pbp