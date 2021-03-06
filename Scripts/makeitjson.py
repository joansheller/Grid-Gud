from helpers import findpath, averagex_andy, get_closest_cable, check_further

# output the results in json format
def makejson(batteries):
    jsonlist = []

    # loop over batteries
    for item in batteries:
        battery = batteries[item]

        # create a dict for the battery
        batterydict = {
            'locatie' : battery.coord,
            'capaciteit' : battery.capacity,
            'huizen' : []
            }

        # check if horizontal or vertical needs to be done first
        first = averagex_andy(battery)
        # loop over connected houses
        for house in battery.connected_houses:
            
            """For random.py see docstring below"""

            # get all aready laid cables
            all_cables = []
            for houses in batterydict['huizen']:
                all_cables += houses['kabels']

            # check which cable is closest to the house
            start = get_closest_cable(all_cables, house.coord)
            if start == (110, 110):
                start = battery.coord
            
            # Check if there is a house on the same line close to this one
            other = check_further(start, house.coord, battery.connected_houses, first)
            
            # If so, first move horizontal or vertical depending on the found house
            if other != first:
                path = findpath(start, house.coord, other)
            else:
                path = findpath(start, house.coord, first)

            """comment above, un-comment below and vice-versa"""
            # path= findpath(battery.coord, house.coord, first)

            house.path = path

            # make a dict for the house
            batterydict['huizen'].append({
                'locatie' : house.coord,
                'output' : house.output,
                # create the path to the house from the battery
                'kabels' : path
            })
        jsonlist.append(batterydict)

    return jsonlist
