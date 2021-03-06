class Battery():
    def __init__(self, coord, capacity, index):
        self.coord = coord
        self.index = index
        self.capacity = capacity
        self.currentload = 0
        self.connected_houses = []

    def add_house(self, house):

        # add house to connected houses list and flag house as connected
        self.connected_houses.append(house)
        self.currentload += house.output
        house.isconnected = True
        house.batteryconnected = self.index

    def remove_house(self, house):

        # remove house from connected houses list and flag house as disconnected
        self.connected_houses.remove(house)
        self.currentload -= house.output
        house.isconnected = False
        house.batteryconnected = None

    def capacity_check(self, house):

        # check if house can be connected
        if self.currentload + house.output > self.capacity:
            return False
        else:
            return True

    def calculate_distances(self, houses):
        self.distances = []

        # loop over houses
        for house in houses:

            # calculate manhattan distance to houses
            self.distances.append((self.manhatten_distance(self.coord, house.coord), house))
        
        # sort houses on distance
        self.distances.sort(key=lambda tup: tup[0])

    def get_closest_house(self):

        # get closest house that is not connected
        for house in self.distances:
            if house[1].isconnected == True:

                # if battery is connected, remove it from the list
                # this makes the loops shorter on every iteration
                self.distances.remove(house)
            else:
                closest_to_battery = house[1]
                closest_distance = house[0]
                break
        
        # get all not connected houses
        not_connected_houses = [house[1] for house in self.distances if house[1].isconnected == False]

        # loop over already connected houses and not connected houses
        try:
            for house in self.connected_houses:
                for not_connected_house in not_connected_houses:

                    # calc manhatten distance
                    distance = self.manhatten_distance(house.coord, not_connected_house.coord)

                    # update closest house if necessary
                    if distance < closest_distance:
                        closest_distance = distance
                        closest_to_battery = not_connected_house

            # retrun closest house
            return closest_to_battery
        except:
            return None


    def manhatten_distance(self, start, end):

        # calculate manhatten distance
        return abs(start[0] - end[0]) + abs(start[1] - end[1])

    def __str__(self):
        return str(self.coord) + ', ' + str(self.capacity) + ', ' + str(self.currentload) + ', ' + str(len(self.connected_houses))
