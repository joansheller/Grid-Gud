from loadfiles import loadbattery, loadhouse
from makeitjson import makejson
import pprint as pp
from helpers import get_all_cables, get_houses_left, averagex_andy, get_outliers, manhatten_distance, connect_houses,\
    update_battery_location, innit_data, save_highscore
from grid import gridplotter
import random
import json
import copy

highscore_file = '../Scores/wijk3_score_advanced3.txt'
housespath = '../Data/wijk3_huizen.csv'
batterypath = '../Data/wijk3_batterijen.csv'

houseslist = loadhouse(housespath)
batterieslist = loadbattery(batterypath)

batteries, houses = innit_data(houseslist, batterieslist, True, {})

overall_highest = []
overall_highest_score = 1000

for i in range(10):
    print(i)
    highest = []
    highest_score = 1000

    for j in range(10000):
        batteries, houses = innit_data(houseslist, batterieslist, False, batteries)
        batteries, houses, houses_left = connect_houses(batteries, houses)
        if len(houses_left) > 0:
            continue

        result = makejson(batteries)
        score = len(get_all_cables(result))
        if score < highest_score:
            highest_score = score
            highest = result
            best = copy.deepcopy(batteries)
            print('NEW HIGHEST SCORE: ', highest_score, j)
    
    if highest_score < overall_highest_score:
        overall_highest_score = highest_score
        overall_highest = highest
        print('NEW OVERALL HIGHEST SCORE: ', overall_highest_score)

    batteries = copy.deepcopy(best)
    batteries = update_battery_location(batteries)

print(overall_highest_score)
gridplotter(overall_highest)

save_highscore(highscore_file, overall_highest)