# -*- coding: utf-8 -*-
"""
Created on Sun Dec 27 19:30:50 2020

@author: ardyb
"""

import sqlite3 as lite
import pandas as pd
import time
import glob
import re


def create_db(data_path):
    timestr = time.strftime("%Y%m%d")
    daily = glob.glob(data_path + "/*daily_{}.csv".format(timestr))
    weekly = glob.glob(data_path + "/*weekly_{}.csv".format(timestr))
    conn = lite.connect(r'D:\Diddly\Python\Stream\Data\Spotify.db')
    c = conn.cursor()
    
    for daily_country in daily:
        res = re.findall(r'\w+', daily_country)
        daily_sql = '''CREATE TABLE {} (TrackID int PRIMARY KEY, Position int, TrackName text,
                                        Artist text, Streams int, URL float, Appears int, Rank int,
                                        SongIDs int, Danceability float, Energy float, Acousticness float, Analysis_URL text,
                                        Duration_MS int, Spotify_Song_ID int, Instrumentalness float, Key int, Liveness float,
                                        Loudness float, Mode int, Speechiness float, Tempo float,
                                        Time_Signature int, Track_Href text, Search_Type text, URI text,
                                        Valence float, Artist_Genres text)'''.format(res[5])
        c.execute(daily_sql)

        daily = pd.read_csv(daily_country, index_col=[0])
        daily.to_sql('{}'.format(res[5]), conn, if_exists='append', index=False)
        
    for weekly_country in weekly:
        res_weekly = re.findall(r'\w+', weekly_country)
        
        weekly_sql = '''CREATE TABLE {} (TrackID int PRIMARY KEY, Position int, TrackName text,
                                        Artist text, Streams int, URL float, Appears int, Rank int,
                                        SongIDs int, Danceability float, Energy float, Acousticness float, Analysis_URL text,
                                        Duration_MS int, Spotify_Song_ID int, Instrumentalness float, Key int, Liveness float,
                                        Loudness float, Mode int, Speechiness float, Tempo float,
                                        Time_Signature int, Track_Href text, Search_Type text, URI text,
                                        Valence float, Artist_Genres text)'''.format(res_weekly[5])
        c.execute(weekly_sql)
        
        weekly = pd.read_csv(weekly_country, index_col=[0])
        weekly.to_sql('{}'.format(res_weekly[5]), conn, if_exists='append', index=False)
        
        conn.commit()
        
    conn.close()
