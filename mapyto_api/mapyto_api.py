import random
import string
import webbrowser

from geopy.geocoders import Nominatim
from math import radians, acos, sin, cos


class Mapyto:
    def __init__(self, lst=["none"]):
        self.coordinates_list = []
        self.main(lst)

    def _user_agent_generator(self, stringLength=8):
        """Generate a random API key for Nominatim

            Arguments:
                stringLength {int} -- Length of the key

            Returns:
                string -- The random API key
            """

        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(stringLength))

    def get_coordinates(self, address_lst):
        """Generate the list of coordinates

            Arguments:
                adress_lst {list} -- List of addresses

            Returns:
                coordinate_lst -- The list of coordinates
            """

        # Creation of the coordinates list
        for adress in address_lst:
            key = self._user_agent_generator(10)
            geolocator = Nominatim(user_agent=key, timeout=3)
            location = geolocator.geocode(adress)
            self.coordinates_list.append([location.latitude, location.longitude])

    def get_distance(self, a, b, c, d):
        """Convert coordinate into a distance in meters

            Arguments:
                a {int} -- Coordinate x_a
                b {int} -- Coordinate y_a
                c {int} -- Coordinate x_b
                d {int} -- Coordinate y_b

            Returns:
                int -- Distance in meters
            """

        # Conversion of each coordinate into radians
        x_a = radians(a)
        x_b = radians(c)
        y_a = radians(b)
        y_b = radians(d)

        # Calculation of the distance in meters
        distance = 6378137 * acos((sin(x_a) * sin(x_b)) + (cos(x_a) * cos(x_b) * cos(y_b - y_a)))

        return distance

    def sort_addresses(self):
        """Sorting "near by near" of each coordinates

            Arguments:
                lst {list} -- List of the coordinates

            Returns:
                list -- List of the sorted coordinates
            """

        # Initialisation of local variable
        lst_trans = []
        lst_final = []
        i = 1
        j = 0

        # While loop (= to be sure that all of the list is sorted)
        while self.coordinates_list:
            x = len(self.coordinates_list)

            # Creation of an array = [[distance][coordinate]]
            for i in range(1, x):
                lst_1 = self.coordinates_list[0]
                lst_2 = self.coordinates_list[i]
                z = self.get_distance(lst_1[0], lst_1[1], lst_2[0], lst_2[1])
                lst_trans.append([[round(z)], self.coordinates_list[i]])

            # Sorting of the array
            lst_end = sorted(lst_trans, key=lambda colonne: colonne[0])

            # Preparation of the next loop (delete the first value and throw at the begginning the most close value)
            if len(lst_end) != 0:
                lst_final.append(self.coordinates_list[0])
                self.coordinates_list.pop(0)
                x = lst_end[0][1]
                self.coordinates_list.remove(lst_end[0][1])
                self.coordinates_list.append(x)
                self.coordinates_list.reverse()
            else:
                lst_final.append(self.coordinates_list[0])
                break

            # Erasing of the local variable for next loop
            lst_end = []
            lst_trans = []

            j += 1

        return lst_final

    def main(self, lst=["none"]):
        adresses_list = []
        if lst == ["none"] :
            nbr = int(input("How many adresses do you have to enter ? "))

            for i in range(nbr):
                adress = input(f"Adress n°{i+1} : ")
                adresses_list.append(adress)

        else:
            adresses_list = lst

        self.get_coordinates(adresses_list)
        sorted_coordinates = self.sort_addresses()

        url_bgn = "https://www.google.com/maps/dir"
        link_end = ""
        for i, j in sorted_coordinates:
            link_end += "/" + str(i) + "," + str(j)

        url_end = url_bgn + link_end

        webbrowser.open(url_end)


if __name__ == "__main__":
    mp = Mapyto(["Paris", "Berlin", "Dijon", "Amsterdam", "Oslo", "Bruxelles", "Cologne", "Hambourg", "Varsovie", "Helsinki"])