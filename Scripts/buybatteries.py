from loadfiles import loadbattery, loadhouse
from makeitjson import makejson
import random
from helpers import innit_data, update_battery_location, connect_houses, get_all_cables, save_highscore, make_boxplot, scores_plot
from grid import gridplotter

highscore_file = '../Scores/wijk2_score_buy_batteries.txt'
housespath = '../Data/wijk2_huizen.csv'
batterypath = '../Data/wijk2_batterijen.csv'

# load houses
houseslist = loadhouse(housespath)

# set battery options
battery_options = [
    {'price' : 900, 'capacity': 450},
    {'price' : 1350, 'capacity': 900},
    {'price' : 1800, 'capacity': 1800}
]

# set highest score variables
highest_score = 1000
highest_cap = 0
highest_battery_combo = []
highest_price = 0
scores = []

# try 10 battery locations
for i in range(10):
    
    total_cap = 0
    battery_combo = []
    price = 0

    # choose batteries until enough capacity is reached
    while total_cap < 7500:
        battery = random.choice(battery_options)
        total_cap += battery['capacity']
        price += battery['price']
        battery_combo.append([100, 100, battery['capacity']])

        batteries, houses = innit_data(houseslist, battery_combo, True, {})

        batteries, houses, houses_left = connect_houses(batteries, houses)

    # try to get a high score
    for j in range(1000):

        # clean batteries and houses for next loop
        batteries, houses = innit_data(houseslist, battery_combo, False, batteries)

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
            highest_battery_combo = battery_combo
            highest_cap = total_cap
            highest_price = price
    


# get results in json format
print(f'Capacity: {highest_cap}, price: {highest_price}, battery combo: {highest_battery_combo}. Highest score for setup: {highest_score}')

# Visualize the result
gridplotter(highest)

# save the new highscore
save_highscore(highscore_file, highest)

# plot all scores
scores_plot(scores)

# make a boxplot of all scores
make_boxplot(scores)
