from geopy.exc import GeocoderTimedOut 
from geopy.geocoders import Nominatim 
import os
import glob
import pandas as pd

# versions used: geopy 1.10.0, pandas 0.16.2, python 2.7.8

data_directory = path + "/Data"

def geocode(path):
    timestr = time.strftime("%Y%m%d")

    # destination_folder = "D:\Diddly\Python\Stream\Data"
    daily = glob.glob(final_directory + "/*daily_{}.csv".format(timestr)) # Include slash or it will search in the wrong directory!!
    weekly = glob.glob(final_directory + "/*weekly_{}.csv".format(timestr)) # Include slash or it will search in the wrong directory!!

    # declare an empty list to store 
    # latitude and longitude of values  
    # of city column 
    daily_longitude = [] 
    daily_latitude = []
    weekly_longitude = [] 
    weekly_latitude = [] 
    
    # function to find the coordinate 
    # of a given city  
    def findGeocode(city): 
        
        # try and catch is used to overcome 
        # the exception thrown by geolocator 
        # using geocodertimedout   
        try: 
            
            # Specify the user_agent as your 
            # app name it should not be none 
            geolocator = Nominatim(user_agent="spotify_countries") 
            
            return geolocator.geocode(city) 
        
        except GeocoderTimedOut: 
            
            return findGeocode(city)     
    
    # each value from city column 
    # will be fetched and sent to 
    # function find_geocode    
    for i in (df["City"]): 
        
        if findGeocode(i) != None: 
            
            loc = findGeocode(i) 
            
            # coordinates returned from  
            # function is stored into 
            # two separate list 
            latitude.append(loc.latitude) 
            longitude.append(loc.longitude) 
        
        # if coordinate for a city not 
        # found, insert "NaN" indicating  
        # missing value  
        else: 
            latitude.append(np.nan) 
            longitude.append(np.nan)
