import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
from googletrans import Translator, constants
from geopy.exc import GeocoderTimedOut 
from geopy.geocoders import Nominatim 
import pandas as pd
import numpy as np
import time
import glob
import re
import os

# uppercase_countries = (
#     "AD","AR","AU","AT","BE",
#     "BO","BR","BG","CA","CL",
#     "CO","CR","CY","CZ","DK",
#     "DO","EC","SV","EE","FI",
#     "FR","DE","GR","GT","HN",
#     "HK","HU","ID","IS","IE","IT",
#     "JP","LV","LI","LT","LU","MY",
#     "MT","MX","MC","NL","NZ", "NI",
#     "NO","PA","PY","PE", "PH","PL",
#     "PT","ES","SG", "SK","SE","CH",
#     "TW","TR", "GB","US","UY")
#
# all_markets = {
# "ad": "Andorra","ar": "Argentina","au": "Australia", "at": "Austria",
# "be": "Belgium","bo": "Bolivia", "br": "Brazil", "bg": "Bulgaria",
# "ca": "Canada","cl": "Chile","co": "Colombia","cr": "Costa Rica",
# "cy": "Cyprus","cz": "Czech Republic","dk": "Denmark","do": "Dominican Republic",
# "ec": "Ecuador","sv": "El Salvador","ee": "Estonia","fi": "Finland",
# "fr": "France","de": "Germany","gr": "Greece","gt": "Guatemala",
# "hn": "Honduras","hk": "Hong Kong","hu": "Hungary","id": "Indonesia",
# "is": "Iceland","ie": "Republic of Ireland","it": "Italy",
# "jp": "Japan","lc": "Latvia","li": "Liechtenstein","lt": "Lithuania",
# "lu": "Luxembourg","my": "Malaysia","mt": "Malta","mw": "Mexico",
# "mc": "Monaco","nl": "Netherlands","nz": "New Zealand","ni": "Nicaragua",
# "no": "Norway","pa": "Panama","py": "Paraguay","pe": "Peru",
# "ph": "Philippines","pl": "Poland","pt": "Portugal","es": "Spain",
# "sg": "Singapore","sk": "Slovakia","se": "Sweden","ch": "Switzerland",
# "tw": "Taiwan","tr": "Turkey","gb": "United Kingdom","us": "United States",
# "uy": "Uruguay"
# }

uppercase_countries = {
    "JP",
    "US"
}

all_markets = {
    "jp": "Japan",
    "us": "United States"
}

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id='', client_secret=''))
translator = Translator(service_urls=['translate.googleapis.com'])

current_directory = os.getcwd()
final_directory = os.path.join(current_directory, r'Data')
if not os.path.exists(final_directory):
    os.makedirs(final_directory)


# function to find the coordinate of a given city
def findGeocode(city):
    # try and catch is used to overcome the exception thrown by geolocator using geocodertimedout
    try: 
        
        # Specify the user_agent as your 
        # app name it should not be none 
        geolocator = Nominatim(user_agent="spotify_countries") 
        
        return geolocator.geocode(city) 
    
    except GeocoderTimedOut: 
        
        return findGeocode(city)


def SongRankings(path):
    timestr = time.strftime("%Y%m%d")
    
    # destination_folder = "D:\Diddly\Python\Stream\Data"
    daily = glob.glob(final_directory + "/*daily_{}.csv".format(timestr))
    weekly = glob.glob(final_directory + "/*weekly_{}.csv".format(timestr))

    for country_daily in daily:
        ### Read input files
        top_songs_daily = pd.read_csv(country_daily,
                                        skiprows=range(0,1))

        top_songs_daily = top_songs_daily.loc[:, ~top_songs_daily.columns.str.contains('^0.')]
        
        ### Counting Artist based off number of tracks
        artist_count_daily = top_songs_daily.Artist.value_counts()
        artist_count_daily = artist_count_daily.to_dict()
        top_songs_daily['Appears'] = top_songs_daily.Artist.map(artist_count_daily)
        top_songs_daily.sort_values(['Appears'], inplace=True, ascending=False)
        
        ### Creating string combination for amount of times Artist showed up and number of streams 
        rank_daily = top_songs_daily['Appears'].astype(str)
        streams_daily = top_songs_daily['Streams'].astype(str)
        
        ### Use 'max' rank in pd to pull the highest rank in the group & output files
        top_songs_daily['Rank'] = (rank_daily+streams_daily).astype(int).rank(method='max', ascending=False).astype(int)
        top_songs_daily = top_songs_daily.sort_values('Rank')
        top_songs_daily.rename(columns = {'Track Name':'TrackName'}, inplace = True)
        top_songs_daily.insert(0, 'TrackID', range(0, 0 + len(top_songs_daily)))

        top_songs_daily.to_csv(country_daily)
    
    for country_weekly in weekly:
        ### Read input files
       top_songs_weekly = pd.read_csv(country_weekly,
                                      skiprows=range(0,1))

       top_songs_weekly = top_songs_weekly.loc[:, ~top_songs_weekly.columns.str.contains('^0.')]
       
       ### Counting Artist based off number of tracks
       artist_count_weekly = top_songs_weekly.Artist.value_counts()
       artist_count_weekly = artist_count_weekly.to_dict()
       top_songs_weekly['Appears'] = top_songs_weekly.Artist.map(artist_count_weekly)
       top_songs_weekly.sort_values(['Appears'], inplace=True, ascending=False)
       
       ### Creating string combination for amount of times Artist showed up and number of streams 
       rank_weekly = top_songs_weekly['Appears'].astype(str)
       streams_weekly = top_songs_weekly['Streams'].astype(str)
       
       ### Use 'max' rank in pd to pull the highest rank in the group & output files
       top_songs_weekly['Rank'] = (rank_weekly+streams_weekly).astype(int).rank(method='max', ascending=False).astype(int)
       top_songs_weekly = top_songs_weekly.sort_values('Rank')
       top_songs_weekly.rename(columns = {'Track Name':'TrackName'}, inplace = True)
       top_songs_weekly.insert(0, 'TrackID', range(0, 0 + len(top_songs_weekly)))

       top_songs_weekly.to_csv(country_weekly)


def SongAttributes(path):
    timestr = time.strftime("%Y%m%d")
    
    # destination_folder = "D:\Diddly\Python\Stream\Data"
    daily = glob.glob(final_directory + "/*daily_{}.csv".format(timestr))
    weekly = glob.glob(final_directory + "/*weekly_{}.csv".format(timestr))

    for country_daily in daily:
        top_songs_daily = pd.read_csv(country_daily)
        
        daily_song_urls = list(top_songs_daily.URL)
        daily_song_ids = []
        
        daily_danceability = []
        daily_energy = []
        daily_acousticness = []
        daily_analysis_url = []
        daily_duration = []
        daily_song_id = []
        daily_instrumentalness = []
        daily_key = []
        daily_liveness = []
        daily_loundess = []
        daily_mode = []
        daily_speechiness = []
        daily_tempo = []
        daily_time_signature = []
        daily_track_href = []
        daily_search_type = []
        daily_uri = []
        daily_valence = []
        
        for daily_url_id in daily_song_urls:
            res = re.findall(r'\w+', daily_url_id)
            daily_song_ids.append(res[5])
        
        top_songs_daily['SongIDs'] = daily_song_ids
        
        daily_songs_attributes = []
        
        for d_song_id in top_songs_daily.SongIDs:
            d_song_info = sp.audio_features(d_song_id)
            daily_songs_attributes.append(d_song_info)
            
        for daily_attribute in daily_songs_attributes:
            daily_danceability.append(daily_attribute[0]['danceability'])
            daily_energy.append(daily_attribute[0]['energy'])
            daily_acousticness.append(daily_attribute[0]['acousticness'])
            daily_analysis_url.append(daily_attribute[0]['analysis_url'])
            daily_duration.append(daily_attribute[0]['duration_ms'])
            daily_song_id.append(daily_attribute[0]['id'])
            daily_instrumentalness.append(daily_attribute[0]['instrumentalness'])
            daily_key.append(daily_attribute[0]['key'])
            daily_liveness.append(daily_attribute[0]['liveness'])
            daily_loundess.append(daily_attribute[0]['loudness'])
            daily_mode.append(daily_attribute[0]['mode'])
            daily_speechiness.append(daily_attribute[0]['speechiness'])
            daily_tempo.append(daily_attribute[0]['tempo'])
            daily_time_signature.append(daily_attribute[0]['time_signature'])
            daily_track_href.append(daily_attribute[0]['track_href'])
            daily_search_type.append(daily_attribute[0]['type'])
            daily_uri.append(daily_attribute[0]['uri'])
            daily_valence.append(daily_attribute[0]['valence'])
        
        top_songs_daily['Danceability'] = daily_danceability
        top_songs_daily['Energy'] = daily_energy
        top_songs_daily['Acousticness'] = daily_acousticness
        top_songs_daily['Analysis_URL'] = daily_analysis_url
        top_songs_daily['Duration_MS'] = daily_duration
        top_songs_daily['Spotify_Song_ID'] = daily_song_id
        top_songs_daily['Instrumentalness'] = daily_instrumentalness
        top_songs_daily['Key'] = daily_key
        top_songs_daily['Liveness'] = daily_liveness
        top_songs_daily['Loudness'] = daily_loundess
        top_songs_daily['Mode'] = daily_mode
        top_songs_daily['Speechiness'] = daily_speechiness
        top_songs_daily['Tempo'] = daily_tempo
        top_songs_daily['Time_Signature'] = daily_time_signature
        top_songs_daily['Track_Href'] = daily_track_href
        top_songs_daily['Search_Type'] = daily_search_type
        top_songs_daily['URI'] = daily_uri
        top_songs_daily['Valence'] = daily_valence

        artist_genres_daily = []
        tmp_artists_daily = list(top_songs_daily.Artist)
        
        for artist_daily in tmp_artists_daily:
            translation_daily = translator.translate("{}".format(artist_daily))
            result_daily = sp.search('{}'.format(translation_daily.text), limit=1, type='artist')
            artists_d = result_daily['artists']
            if artists_d['items'] == []:
                artist_genres_daily.append('')
            else:
                artist_genres_daily.append(artists_d['items'][0]['genres'])
        
        top_songs_daily['Artist_Genres'] = artist_genres_daily

        top_songs_daily.to_csv(country_daily)
        top_songs_daily.drop(top_songs_daily.iloc[:, 0:1], inplace=True, axis=1)

    for country_weekly in weekly:
       top_songs_weekly = pd.read_csv(country_weekly)

       weekly_song_urls = list(top_songs_weekly.URL)
       weekly_song_ids = []
       
       weekly_danceability = []
       weekly_energy = []
       weekly_acousticness = []
       weekly_analysis_url = []
       weekly_duration = []
       weekly_song_id = []
       weekly_instrumentalness = []
       weekly_key = []
       weekly_liveness = []
       weekly_loundess = []
       weekly_mode = []
       weekly_speechiness = []
       weekly_tempo = []
       weekly_time_signature = []
       weekly_track_href = []
       weekly_search_type = []
       weekly_uri = []
       weekly_valence = []
        
       for weekly_url_id in weekly_song_urls:
           res = re.findall(r'\w+', weekly_url_id)
           weekly_song_ids.append(res[5])
    
       top_songs_weekly['SongIDs'] = weekly_song_ids
       
       weekly_songs_attributes = []
        
       for w_song_id in top_songs_weekly.SongIDs:
           w_song_info = sp.audio_features(w_song_id)
           weekly_songs_attributes.append(w_song_info)
            
       for weekly_attribute in weekly_songs_attributes:
           weekly_danceability.append(weekly_attribute[0]['danceability'])
           weekly_energy.append(weekly_attribute[0]['energy'])
           weekly_acousticness.append(weekly_attribute[0]['acousticness'])
           weekly_analysis_url.append(weekly_attribute[0]['analysis_url'])
           weekly_duration.append(weekly_attribute[0]['duration_ms'])
           weekly_song_id.append(weekly_attribute[0]['id'])
           weekly_instrumentalness.append(weekly_attribute[0]['instrumentalness'])
           weekly_key.append(weekly_attribute[0]['key'])
           weekly_liveness.append(weekly_attribute[0]['liveness'])
           weekly_loundess.append(weekly_attribute[0]['loudness'])
           weekly_mode.append(weekly_attribute[0]['mode'])
           weekly_speechiness.append(weekly_attribute[0]['speechiness'])
           weekly_tempo.append(weekly_attribute[0]['tempo'])
           weekly_time_signature.append(weekly_attribute[0]['time_signature'])
           weekly_track_href.append(weekly_attribute[0]['track_href'])
           weekly_search_type.append(weekly_attribute[0]['type'])
           weekly_uri.append(weekly_attribute[0]['uri'])
           weekly_valence.append(weekly_attribute[0]['valence'])
       
       
       top_songs_weekly['Danceability'] = weekly_danceability
       top_songs_weekly['Energy'] = weekly_energy
       top_songs_weekly['Acousticness'] = weekly_acousticness
       top_songs_weekly['Analysis_URL'] = weekly_analysis_url
       top_songs_weekly['Duration_MS'] = weekly_duration
       top_songs_weekly['Spotify_Song_ID'] = weekly_song_id
       top_songs_weekly['Instrumentalness'] = weekly_instrumentalness
       top_songs_weekly['Key'] = weekly_key
       top_songs_weekly['Liveness'] = weekly_liveness
       top_songs_weekly['Loudness'] = weekly_loundess
       top_songs_weekly['Mode'] = weekly_mode
       top_songs_weekly['Speechiness'] = weekly_speechiness
       top_songs_weekly['Tempo'] = weekly_tempo
       top_songs_weekly['Time_Signature'] = weekly_time_signature
       top_songs_weekly['Track_Href'] = weekly_track_href
       top_songs_weekly['Search_Type'] = weekly_search_type
       top_songs_weekly['URI'] = weekly_uri
       top_songs_weekly['Valence'] = weekly_valence
       
       artist_genres_weekly = []
       tmp_artists_weekly = list(top_songs_weekly.Artist)
        
       for artist_weekly in tmp_artists_weekly:
           translation_weekly = translator.translate("{}".format(artist_weekly))
           result_weekly = sp.search('{}'.format(translation_weekly.text), limit=1, type='artist')
           artists_w = result_weekly['artists']
           if artists_w['items'] == []:
               artist_genres_weekly.append('')
           else:
               artist_genres_weekly.append(artists_w['items'][0]['genres'])
        
       top_songs_weekly['Artist_Genres'] = artist_genres_weekly
       top_songs_weekly.to_csv(country_weekly)

def Geocode(path):
    timestr = time.strftime("%Y%m%d")
    
    # destination_folder = "D:\Diddly\Python\Stream\Data"
    daily = glob.glob(final_directory + "/*daily_{}.csv".format(timestr)) # Include slash or it will search in the wrong directory!!
    weekly = glob.glob(final_directory + "/*weekly_{}.csv".format(timestr)) # Include slash or it will search in the wrong directory!!

    for country_daily in daily:
        top_songs_daily = pd.read_csv(country_daily)

        head_tail = os.path.split(country_daily)[1]
        country_code = head_tail.split('_', 1)[0].replace('.', '').lower()

        if country_code in all_markets:
            country_name = all_markets[country_code]
            top_songs_daily['Country'] = country_name

        # each value from city column 
        # will be fetched and sent to 
        # function find_geocode
        daily_longitude = [] 
        daily_latitude = []
        
        for i in (top_songs_daily["Country"]): 
            
            if findGeocode(i) is not None:
                
                loc = findGeocode(i) 
                
                # coordinates returned from  
                # function is stored into 
                # two separate list 
                daily_latitude.append(loc.latitude) 
                daily_longitude.append(loc.longitude) 
            
            # if coordinate for a city not 
            # found, insert "NaN" indicating  
            # missing value  
            else: 
                daily_latitude.append(np.nan) 
                daily_longitude.append(np.nan)

        top_songs_daily["Latitude"] = daily_latitude
        top_songs_daily["Longitude"] = daily_longitude

        top_songs_daily.drop(top_songs_daily.iloc[:, 0:1], inplace=True, axis=1)
        top_songs_daily.to_csv(country_daily)

    for country_weekly in weekly:
       top_songs_weekly = pd.read_csv(country_weekly)

       head_tail = os.path.split(country_daily)[1]
       country_code = head_tail.split('_', 1)[0].replace('.', '').lower()
       
       if country_code in all_markets:
           country_name = all_markets[country_code]
           top_songs_weekly['Country'] = country_name
           
       weekly_longitude = [] 
       weekly_latitude = [] 

       for i in (top_songs_weekly["Country"]):
            if findGeocode(i) != None: 
                
                loc = findGeocode(i) 
                
                # coordinates returned from  
                # function is stored into 
                # two separate list 
                weekly_latitude.append(loc.latitude) 
                weekly_longitude.append(loc.longitude) 
            
            # if coordinate for a city not 
            # found, insert "NaN" indicating  
            # missing value  
            else: 
                weekly_latitude.append(np.nan) 
                weekly_longitude.append(np.nan)
               
       top_songs_weekly["Latitude"] = weekly_longitude
       top_songs_weekly["Longitude"] = weekly_latitude

       top_songs_weekly.drop(top_songs_weekly.iloc[:, 0:1], inplace=True, axis=1)
       top_songs_weekly.to_csv(country_weekly)
