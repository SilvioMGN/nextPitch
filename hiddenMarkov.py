# Hidden Markov Model for Pitch Predictions

import pandas as pd
import math
import numpy as np

# Calculate the transition probability of moving from state i to state j
# Here: The probability that Pitch i is followed by Pitch j
# Design choice: At the moment we consider all pitches of a pitcher in a game as a sequence of pitches, but we could further divide them into at-bat sequences, which seems to be closer to reality.
# The reason for this is that the choice of pitches should be fairly specific, depending on who the opposing batter is?!


def transitionProbabilities(pbp):

    # There are some pitches that are not classified which we ignore
    pbp = pbp[pbp['pitch_name'].notna()]

    allPitcherPercentages = {}

    unqiuePitchers = pbp['pitcher'].unique()

    for pitcher in unqiuePitchers:

        allPitcherPercentages[pitcher] = {}

        allPitches = pbp[pbp['pitcher'] == pitcher]

        print("New Pitcher: " + str(pitcher))

        pitches = allPitches[['pitch_number', 'game_date', 'pitch_name']]
        unqiueGames = allPitches['game_date'].unique()

        for game in unqiueGames:

            # how many pitches were thrown by the pitcher in one game
            numPitchesInGame = len(
                allPitches[allPitches['game_date'] == game])
            # full pitch sequence in one game
            pitchListGame = list(
                pitches[pitches['game_date'] == game]['pitch_name'])

            for i in range(numPitchesInGame-1):

                currentPitch = pitchListGame[i]
                previousPitch = pitchListGame[i+1]

                if currentPitch != "Eephus" and previousPitch != "Eephus":

                    if previousPitch not in allPitcherPercentages[pitcher]:

                        allPitcherPercentages[pitcher][previousPitch] = {'4-Seam Fastball': 0,
                                                                             'Fastball': 0,
                                                                             'Sinker': 0,
                                                                             'Slider': 0,
                                                                             'Split-Finger': 0,
                                                                             'Knuckle Curve': 0,
                                                                             'Knuckleball': 0,
                                                                             'Curveball': 0,
                                                                             'Cutter': 0,
                                                                             'Changeup': 0}

                    allPitcherPercentages[pitcher][previousPitch][currentPitch] += 1

        for key in allPitcherPercentages:

            for previousPitch in allPitcherPercentages[key]:
                sumPitch = sum(
                    allPitcherPercentages[key][previousPitch].values())
                for pitch in allPitcherPercentages[key][previousPitch]:
                    pitchNum = allPitcherPercentages[key][previousPitch][pitch]

                    allPitcherPercentages[key][previousPitch][pitch] = pitchNum/sumPitch

    return allPitcherPercentages


# Calculate the emission probability expressing the probability of an observation o_t being generated from a state i
# Here: The probability of the count given Pitch i
def emissionProbabilities():

    return 1
