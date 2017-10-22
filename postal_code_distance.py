import requests
import googlemaps
import json
from datetime import datetime
import logging


class PostalCodeDistance():
    MODE = "driving"
    UNITS = 'imperial'
    ALTERNATIVES = 'True'
    METERS_IN_A_MILE = 1600

    def __init__(self,postal_code_data, api_key):
        self.base_postcoder = 'https://mapit.mysociety.org/postcode/'
        self.postal_code_data = postal_code_data
        self.client = googlemaps.Client(api_key)
        logging.warning(self.client)


    def get_postal_codes(self, data):
            # returns a list of lists where each list is a line in data
            postal_code_list = []
            for line in data.splitlines():
                postal_code_list.append(line.replace(" ", "").upper().split("TO"))
            return postal_code_list

    def get_lat_long_list(self,postal_code_list):
        #takes a list of postal codes and returns a list of corresponding lat/long
        lat_long_list = []
        for code in postal_code_list:
            code_response = requests.get(self.base_postcoder+code)
            code_data = code_response.json()
            # test if 404
            if 'code' in code_data :
               return 0
            else :
               lat_long_list.append("{},{}".format(code_data['wgs84_lat'], code_data['wgs84_lon']))
        return lat_long_list

    def get_distance(self,single_list, route_choice):
        if single_list == 0:
            return 0
        total_distance = 0
        for key in range(1,len(single_list)):
            best_route = self.get_best_route_distance(single_list[key-1], single_list[key], route_choice)
            total_distance = total_distance + best_route
        return total_distance

    def get_best_route_distance(self,start, finish, route_choice):
        routes = self.client.directions(start, finish, mode=self.MODE,
            alternatives=self.ALTERNATIVES,units=self.UNITS)
        distances = []
        total_time_list = []
        for route in routes:
            total_distance = 0
            total_time = 0
            for leg in route['legs']:
                total_distance = total_distance + leg['distance']['value']
                total_time = total_time + leg['duration']['value']
                total_time_list.append(total_time)
                distances.append(total_distance)
        if route_choice == 'shortest':
            return min(distances)
        else:
            index_of_fastest = total_time_list.index(min(total_time_list))
            return distances[index_of_fastest]


    def get_list_of_distances(self, route_choice):
            lat_long_lists =[]
            list_of_distances = []
            postal_code_lists = self.get_postal_codes(self.postal_code_data)
            for line in postal_code_lists:
                lat_long_lists.append(self.get_lat_long_list(line))
            for single_list in lat_long_lists:
                list_of_distances.append(self.get_distance(single_list,route_choice) / self.METERS_IN_A_MILE)
            return list(map(lambda x: round(x, 1), list_of_distances)) #round distances for presentation

    def generate_csv_data(self, postal_code_list, list_of_distances,route_choice):
        csv_data = []
        max_length = len(max(postal_code_list,key=len))
        csv_row = []
        for column in range(max_length):
            csv_row.append("Postal Code " + str(column+1))
        csv_row.append("Distance")
        csv_row.append("Route Choice")
        csv_data.append(csv_row)
        for key, code_list in enumerate(postal_code_list):
            csv_row = []
            for column in range(max_length):
                if column < len(code_list):
                    csv_row.append(code_list[column])
                else: csv_row.append("")
            csv_row.append(list_of_distances[key])
            csv_row.append(route_choice)
            csv_data.append(csv_row)
        return csv_data
