import sqlite3 as lite
import pandas as pd
import time
import glob
import re
import os

def CreateDB(path):
    current_directory = os.getcwd()
    csv_directory = os.path.join(current_directory, r'Data')
    conn = lite.connect(r'D:\Diddly\Python\GlobalTracks\sql_con\Spotify_Rankings.db')
    c = conn.cursor()

    daily = glob.glob(csv_directory + "/*daily_*.csv")
    weekly = glob.glob(csv_directory + "/*weekly_*.csv")

    for daily_country in daily:
        res = re.findall(r'\w+', daily_country)
        daily_sql = '''CREATE TABLE {} (TrackID int PRIMARY KEY, Position int, TrackName text,
                                                Artist text, Streams int, URL float, Appears int, Rank int,
                                                SongIDs int, Danceability float, Energy float, Acousticness float, Analysis_URL text,
                                                Duration_MS int, Spotify_Song_ID int, Instrumentalness float, Key int, Liveness float,
                                                Loudness float, Mode int, Speechiness float, Tempo float,
                                                Time_Signature int, Track_Href text, Search_Type text, URI text,
                                                Valence float, Artist_Genres text, Country text, Latitude real, Longitude real)'''.format(
            res[5])

        c.execute(daily_sql)

        conn.commit()

    for weekly_country in weekly:
        res_weekly = re.findall(r'\w+', weekly_country)

        weekly_sql = '''CREATE TABLE {} (TrackID int PRIMARY KEY, Position int, TrackName text,
                                                Artist text, Streams int, URL float, Appears int, Rank int,
                                                SongIDs int, Danceability float, Energy float, Acousticness float, Analysis_URL text,
                                                Duration_MS int, Spotify_Song_ID int, Instrumentalness float, Key int, Liveness float,
                                                Loudness float, Mode int, Speechiness float, Tempo float,
                                                Time_Signature int, Track_Href text, Search_Type text, URI text,
                                                Valence float, Artist_Genres text, Country text, Latitude real, Longitude real)'''.format(
            res_weekly[5])
        c.execute(weekly_sql)
        
    conn.close()


def UpdateDB(path):
    current_directory = os.getcwd()
    csv_directory = os.path.join(current_directory, r'Data')
    conn = lite.connect(r'D:\Diddly\Python\GlobalTracks\sql_con\Spotify_Rankings.db')

    daily = glob.glob(csv_directory + "/*daily_*.csv")
    weekly = glob.glob(csv_directory + "/*weekly_*.csv")

    for daily_country in daily:
        res = re.findall(r'\w+', daily_country)
        daily = pd.read_csv(daily_country, index_col=[0])
        daily.to_sql('{}'.format(res[5]), conn, if_exists='append', index=False)

    for weekly_country in weekly:
        res_weekly = re.findall(r'\w+', weekly_country)
        weekly = pd.read_csv(weekly_country, index_col=[0])
        weekly.to_sql('{}'.format(res_weekly[5]), conn, if_exists='append', index=False)