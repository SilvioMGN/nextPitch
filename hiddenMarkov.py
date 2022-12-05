# Hidden Markov Model for Pitch Predictions

import pandas as pd
import math
import numpy as np

# Calculate the transition probability of moving from state i to state j
# Here: The probability that Pitch i is followed by Pitch j

# Design choice: At the moment we consider all pitches of a pitcher in a game as a sequence of pitches, but we could further divide them into at-bat sequences, which seems to be closer to reality.
# The reason for this is that the choice of pitches should be fairly specific, depending on who the opposing batter is?!


def transitionProbabilities(pbp, pitcher):

    # There are some pitches that are not classified which we ignore
    pbp = pbp[pbp['pitch_name'].notna()]

    pitcherPercentage = {}

    allPitches = pbp[pbp['player_name_y'] == pitcher]

    pitches = allPitches[['pitch_number', 'game_date', 'pitch_name']]
    unqiueGames = allPitches['game_date'].unique()

    unqiuePitches = allPitches['pitch_name'].unique()
                    
    for i in range(len(unqiuePitches)):
        pitcherPercentage[unqiuePitches[i]] = {}
        for j in range(len(unqiuePitches)):
            pitcherPercentage[unqiuePitches[i]].update({unqiuePitches[j]: 0}) 

    for game in unqiueGames:

        # how many pitches were thrown by the pitcher in one game
        numPitchesInGame = len(allPitches[allPitches['game_date'] == game])
        # full pitch sequence in one game
        pitchListGame = list(
            pitches[pitches['game_date'] == game]['pitch_name'])

        for i in range(numPitchesInGame-1):

            currentPitch = pitchListGame[i]
            previousPitch = pitchListGame[i+1]

            if currentPitch != "Eephus" and previousPitch != "Eephus":

                if previousPitch not in pitcherPercentage:                      

                    '''pitcherPercentage[previousPitch] = {'4-Seam Fastball': 0,
                                                                     'Fastball': 0,
                                                                     'Sinker': 0,
                                                                     'Slider': 0,
                                                                     'Split-Finger': 0,
                                                                     'Knuckle Curve': 0,
                                                                     'Knuckleball': 0,
                                                                     'Curveball': 0,
                                                                     'Cutter': 0,
                                                                     'Changeup': 0}'''

                pitcherPercentage[previousPitch][currentPitch] += 1

    for previousPitch in pitcherPercentage.keys():
        sumPitch = sum(pitcherPercentage[previousPitch].values())
        for pitch in pitcherPercentage[previousPitch]:
                pitchNum = pitcherPercentage[previousPitch][pitch]

                pitcherPercentage[previousPitch][pitch] = pitchNum/sumPitch

    return pitcherPercentage


# Calculate the emission probability expressing the probability of an observation o_t being generated from a state i
# Here: The probability of the count given Pitch i
def emissionProbabilities(pbp, pitcher):

    # There are some pitches that are not classified which we ignore
    pbp = pbp[pbp['pitch_name'].notna()]
    pbp = pbp[pbp['player_name_y'] == pitcher]

    countPitch = {}

    pitches = pd.DataFrame(pbp)
    pitches = pitches.reset_index()

    for index, row in pitches.iterrows():

        # New variable to give count
        count = str(row['balls']) + "-" + str(row['strikes'])

        if row['pitcher'] not in countPitch.keys():
            countPitch[row['pitcher']] = {}
        if row['pitch_name'] not in countPitch[row['pitcher']].keys():
            countPitch[row['pitcher']][row['pitch_name']] = {}

        if count not in countPitch[row['pitcher']][row['pitch_name']].keys():
            countPitch[row['pitcher']][row['pitch_name']][count] = 0

        # Count the times a pitch has been thrown in a count
        countPitch[row['pitcher']][row['pitch_name']][count] += 1

    return countPitch

# Calculate probability of next state


def forwardAlgorithm(data, transition, emission, initialDistribution):
    
    p = 1
    counts = ['pitch', '0-0', '0-1', '0-2', '1-0', '1-1', '1-2', '2-0', '2-1', '2-2', '3-0', '3-1', '3-2']

    keys = transition.keys()

    # transition dict to matrix
    transisitonMatrix = np.array([transition[i] for i in keys])

    values = list(emission.values())
    keys = values[0].keys()

    emissionMatrix = []

    # emission dict to matrix
    for key in keys:
        tempList = []
        for i in counts: 
            if i == 'pitch':
                tempList.append(key)
            elif i in values[0][key]:   
                tempList.append(values[0][key][i])
            else:
                tempList.append(0)

        emissionMatrix.append(tempList)


    # data.shape[0] indicates the length of the data set, i.e. the total number of pitches of the specified pitcher
    # transitionMatrix.shape[0] gives us the number of pitch types used by the pitcher

    alpha = np.zeros((data.shape[0], transisitonMatrix.shape[0]))
    alpha[0, :] = initialDistribution * emission[:, data[0]]

    for t in range(1, data.shape[0]):
        probability_of_observation = 0 
        for j in range(transition.shape[0]):
            alpha[t, j] = alpha[t - 1].dot(transition[:, j]) * emission[j, data[t]]
            probability_of_observation += alpha[t, j]  
        p = p * probability_of_observation 

    return p #changed
