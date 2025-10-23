import csv
import re
import math
import numpy as np
from sklearn.neighbors import NearestNeighbors

class Cell:
    def __init__(self,CellName,Latitude,Longitude,Azimuth,RRC_Att,RRC_Succ,Timing_Advance,tilt):
        self.CellName = CellName
        self.Latitude = Latitude
        self.Longitude = Longitude
        self.Azimuth = Azimuth
        self.RRC_Att = RRC_Att
        self.RRC_Succ = RRC_Succ
        self.Timing_Advance = Timing_Advance
        self.tilt = tilt
        self.state = "No action"


    def __str__(self):
        return f"{self.CellName}'s state is {self._state}, and its tilt value is {self.tilt}"

    def __eq__(self, compared):                                                                     # for the test purpose, when comparing two instances, it compares their values
        return (
            self.CellName == compared.CellName and
            self.Latitude == compared.Latitude and
            self.Longitude == compared.Longitude and
            self.RRC_Att == compared.RRC_Att and
            self.RRC_Succ == compared.RRC_Succ and
            self.Timing_Advance == compared.Timing_Advance and
            self.tilt == compared.tilt
        )

    def uptilt(self):
        if self.tilt < 20:
            self.tilt = 0
        else:
            self.tilt -= 20
        return self.tilt

    def downtilt(self):
        if self.tilt > 80:
            self.tilt = 100
        else:
            self.tilt += 20
        return self.tilt

    @property
    def Latitude(self):
        return self._Latitude

    @Latitude.setter
    def Latitude(self,Latitude):
        self._Latitude = float(Latitude)

    @property
    def Longitude(self):
        return self._Longitude

    @Longitude.setter
    def Longitude(self,Longitude):
        self._Longitude = float(Longitude)

    @property
    def RRC_Att(self):
        return self._RRC_Att

    @RRC_Att.setter
    def RRC_Att(self,RRC_Att):
        if int(RRC_Att) < 0:
            raise ValueError("RRC_Att value cannot be less than 0")
        else:
            self._RRC_Att = int(RRC_Att)

    @property
    def RRC_Succ(self):
        return self._RRC_Succ

    @RRC_Succ.setter
    def RRC_Succ(self,RRC_Succ):
        if int(RRC_Succ) > self.RRC_Att:
            raise ValueError("RRC_Succ value cannot be greater than RRC_Att")
        elif int(RRC_Succ) < 0:
            raise ValueError("RRC_Succ value cannot be less than 0")
        else:
            self._RRC_Succ = int(RRC_Succ)

    @property
    def Timing_Advance(self):
        return self._Timing_Advance

    @Timing_Advance.setter
    def Timing_Advance(self,Timing_Advance):
        if float(Timing_Advance) > 100:
            raise ValueError("Timing_Advance value cannot be more than 100")
        elif float(Timing_Advance) < 0:
            raise ValueError("Timing_Advance value cannot be less than 0")
        else:
            self._Timing_Advance = float(Timing_Advance)

    @property
    def tilt(self):
        return self._tilt

    @tilt.setter
    def tilt(self,tilt):
        if int(tilt) > 100:
            raise ValueError("Tilt value cannot be more than 100")
        elif int(tilt) < 0:
            raise ValueError("Tilt value cannot be less than 0")
        else:
            self._tilt = int(tilt)

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self,new_state):
        if new_state in ["No action","Overshooter, cell downtilted 20 degrees","Undershooter, cell uptilted 20 degrees",
                         "Overshooter, cell downtilted less than 20 degrees","Undershooter, cell uptilted less than 20 degrees",
                         "Tilt value cannot be increased further","Tilt value cannot be decreased further"]:
            self._state = new_state
        else:
            raise ValueError("Please select a defined state: " \
            "No action, " \
            "Overshooter, " \
            "cell downtilted 20 degrees, " \
            "Undershooter, cell uptilted 20 degrees," \
            "Overshooter, cell downtilted less than 20 degrees," \
            "Undershooter, cell uptilted less than 20 degrees," \
            "Tilt value cannot be increased further, " \
            "Tilt value cannot be decreased further")


def main():
    data = []                                                                   #Place holder for cell list
    data_analyzed = []                                                          #Place holder for analyzed and updated cell list
    data = get_input_data()                                                     #Getting the cell list
    RRC_Threshold = get_RRC_threshold()                                         #Getting the RRC Success Rate threshold for analysis
    neigh_dist = get_closest_neighbor_distance(data)                            #Calculating closest neighbors to compare the given Timing Advance Value
    data_analyzed = analyze_and_update_data(data,neigh_dist,RRC_Threshold)      #Analyzing and updating the data, inputs are list of cells and analysis parameters
    save_output_data(data_analyzed)                                             #Writing the output of the cells in an output file


def get_input_data():
    while True:
        cells =[]
        try:
            input_file = input("What is the source csv file? ")
            with open(input_file) as file:
                reader = csv.DictReader(file)
                for row in reader:
                    cell = Cell(row["CellName"],row["Latitude"],row["Longitude"],row["Azimuth"],row["RRC_Att"],row["RRC_Succ"],row["Timing_Advance"],row["tilt"])  #Creating the cell instances
                    cells.append(cell)    #appending cell instances to a list to hand it over to another function
        except FileNotFoundError:
            print(f"Could not read {input_file}, please try again")
            continue
        return cells


def get_RRC_threshold():
    while True:
        RRC_tresh = input("What is the RRC Success Rate Percentage Threshold? ")
        if (match := re.search(r"^%?(\d\d?)%?$",RRC_tresh)) or (match := re.search(r"^%?(100)%?$",RRC_tresh)):
            return int(match.group(1))
        else:
            print("RRC Success Rate Threshold should be a percentage value between 0 and 100, please try again")
            continue


def get_closest_neighbor_distance(cells):
    closest_neighbor = []                                                                           # Creates an empty list to store and return the names of all cells and the distances of their respective closest neighbor cell in front.
    radian_coordinates = np.radians(np.array([[cell.Longitude, cell.Latitude] for cell in cells]))  # Create a radian numPy ndarray (as Haversine formulation uses radians) consist of the latitude and longitude of the points
    nbrs = NearestNeighbors(n_neighbors=len(cells), metric='haversine').fit(radian_coordinates)     # Created NearestNeighbors object for all neighbors
    distances, indices = nbrs.kneighbors(radian_coordinates)                                        # Neighbor distances and their indices are calculated and stored from closest to farthest
    for i, cell in enumerate(cells):                                                            # Iterating over the source cells to find the first neighbor cell falls within ±60° azimuth in front of source cell.
        source_latitude = math.radians(cell.Latitude)                                           # Convert source cell latitude degrees to radians
        source_longitude = math.radians(cell.Longitude)                                         # Convert source cell longitude degrees to radians
        azi = float(cell.Azimuth)
        minimum_distance = 0
        for k in range(3, len(cells)):                                                          # Iterating over the neighbors, assuming all the source cell locations (sites) have 3 cells, in real life most of the cases like that, but not always.
            neighbor = cells[indices[i, k]]                                                     # Indices array holds the neighbor indices, cells[indices[i,k]] refers to an individual neighbor cell instance in input cells list, for each for loop turn
            neighbor_latitude = math.radians(neighbor.Latitude)                                 # Convert neighbor cell latitude to degrees radians
            neighbor_longitude = math.radians(neighbor.Longitude)                               # Convert neighbor cell longitude to degrees radians
            delta_longitude = neighbor_longitude - source_longitude                             # Mathematical calculation of forward azimuth (bearing) between two points on a sphere
            x = math.sin(delta_longitude) * math.cos(neighbor_latitude)
            y = math.cos(source_latitude) * math.sin(neighbor_latitude) - math.sin(source_latitude) * math.cos(neighbor_latitude) * math.cos(delta_longitude)
            bearing = (math.degrees(math.atan2(x, y)) + 360) % 360
            if min(abs(bearing - azi), 360 - abs(bearing - azi)) <= 60:                         # Checking if the angular difference between azimuth of source cell and bearing between source and neighbor cell is within azimuth ±60° or not
                minimum_distance = distances[i, k] * 6371                                       # if True, set the first valid (nearest) match and break the loop
                break
            else:
                continue
        closest_neighbor.append({"name": cell.CellName, "dist": minimum_distance})              # accumulate the source cell name and closest neighbor distance in a list of dicts to return
    return closest_neighbor


def analyze_and_update_data(cells,neigh_dist,RRC_tresh):
    for cell in cells:
        for dist in neigh_dist:
            if dist["name"] == cell.CellName:
                if (cell.RRC_Succ/cell.RRC_Att)*100 < RRC_tresh and cell.Timing_Advance*1.1 > dist["dist"]:
                    if cell.tilt <= 80:
                        cell.state = "Overshooter, cell downtilted 20 degrees"
                        cell.downtilt()
                    elif 80 < cell.tilt <= 100:
                        cell.state = "Overshooter, cell downtilted less than 20 degrees"
                        cell.downtilt()
                    else:
                        cell.state = "Tilt value cannot be increased further"
                elif (cell.RRC_Succ/cell.RRC_Att)*100 < RRC_tresh and cell.Timing_Advance*0.25 < dist["dist"]:
                    if cell.tilt >= 20:
                        cell.state = "Undershooter, cell uptilted 20 degrees"
                        cell.uptilt()
                    elif 0 < cell.tilt < 20:
                        cell.state = "Undershooter, cell uptilted less than 20 degrees"
                        cell.uptilt()
                    else:
                        cell.state = "Tilt value cannot be decreased further"
                else:
                    continue
    return cells


def save_output_data(cells):
    with open("output.csv","w") as file:
        writer = csv.DictWriter(file, fieldnames=["CellName","Latitude","Longitude","RRC_Att","RRC_Succ","Timing_Advance","tilt","state"])
        writer.writeheader()
        for cell in cells:
            writer.writerow({"CellName" : cell.CellName, "Latitude" : cell.Latitude, "Longitude" : cell.Longitude,"RRC_Att" : cell.RRC_Att,
                             "RRC_Succ" : cell.RRC_Succ, "Timing_Advance" : cell.Timing_Advance, "tilt" : cell.tilt, "state" : cell.state})
    print("Results saved under output.csv")


if __name__ == "__main__":
    main()
