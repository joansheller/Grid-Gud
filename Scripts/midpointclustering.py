from loadfiles import loadbattery, loadhouse
from makeitjson import makejson
from helpers import get_all_cables, get_houses_left, averagex_andy, manhatten_distance, connect_houses,\
    update_battery_location, innit_data, save_highscore, make_boxplot, scores_plot
from grid import gridplotter
import random
import json


highscore_file = '../Scores/wijk1_score_advanced1.txt'
housespath = '../Data/wijk1_huizen.csv'
batterypath = '../Data/wijk1_batterijen.csv'

# load data
houseslist = loadhouse(housespath)
batterieslist = loadbattery(batterypath)

highest_score = 1000
highest = []
attempt = 0
scores = []

# get a relativly good setup for batteries
while highest_score > 610:

    batteries, houses = innit_data(houseslist, batterieslist, True, {})

    batteries, houses, houses_left = connect_houses(batteries, houses)

    if len(houses_left) > 0:
        attempt += 1
        continue

    # get results in json format
    result = makejson(batteries)

    # calculate number of cables
    all_cables = get_all_cables(result)

    # Rememeber highest score
    if len(all_cables) < highest_score:
        highest_score = len(all_cables)
        highest = result

# set best battery setup
for i in range(len(highest)):
    batteries[i].coord = highest[i]['locatie']

# Initialize variables
highest_score_overall = 1000
highest_overall = []
previous_coord = []

# update battery location 100 times
for i in range(10):

    # safe previous coordinates
    previous_coord = [batteries[i].coord for i in batteries]

    # update battery location to middle of its cluster
    batteries = update_battery_location(batteries)
    highest_score = 1000
    highest = []

    # try to get a high score
    for j in range(1000):

        # clean batteries and houses for next loop
        batteries, houses = innit_data(houseslist, batterieslist, False, batteries)

        # make connections
        batteries, houses, houses_left = connect_houses(batteries, houses)

        # if there are houses left, try again
        if len(houses_left) > 0:
            continue

        # make result and get all cables
        result = makejson(batteries)
        all_cables = get_all_cables(result)
        scores.append(len(all_cables))

        # update highest score for current battery location
        if len(all_cables) < highest_score:
            highest_score = len(all_cables)
            highest = result

    highest = makejson(batteries)
    # get score for highest of the battery location
    all_cables = get_all_cables(highest)

    # update highest scores overall
    if len(all_cables) < highest_score_overall and len(all_cables) != 0:
        highest_score_overall = len(all_cables)
        highest_overall = highest 
        print(f'NEW HIGHEST SCORE: {len(all_cables)}')

    print(f'{len(get_all_cables(highest))} for attempt {i}. Starting with {len(get_all_cables(makejson(batteries)))}')



# get results in json format
result = highest_overall

# calculate number of cables
all_cables = get_all_cables(result)

# show score
print(len(all_cables))  

# Visualize result
gridplotter(result)

# Save highest score
save_highscore(highscore_file, result)

# Plot all scores
scores_plot(scores)

# Make boxplot of all scores
make_boxplot(scores)
