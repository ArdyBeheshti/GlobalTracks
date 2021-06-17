# -*- coding: utf-8 -*-
"""
Created on Tue Jun 16 21:18:18 2020

@author: TheSandyOne
"""

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from googletrans import Translator
import pandas as pd
import time
import glob
import re

auth_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(auth_manager=auth_manager)
translator = Translator()


def song_rankings(data_path):
    timestr = time.strftime("%Y%m%d")

    daily = glob.glob(
        data_path + "/*daily_{}.csv".format(timestr))  # Include slash or it will search in the wrong directory!!
    weekly = glob.glob(
        data_path + "/*weekly_{}.csv".format(timestr))  # Include slash or it will search in the wrong directory!!

    for country_daily in daily:
        # Read input files
        top_songs_daily = pd.read_csv(country_daily,
                                      skiprows=range(0, 1))

        # Counting Artist based off number of tracks
        artist_count_daily = top_songs_daily.Artist.value_counts()
        artist_count_daily = artist_count_daily.to_dict()
        top_songs_daily['Appears'] = top_songs_daily.Artist.map(artist_count_daily)
        top_songs_daily.sort_values(['Appears'], inplace=True, ascending=False)

        # Creating string combination for amount of times Artist showed up and number of streams
        rank_daily = top_songs_daily['Appears'].astype(str)
        streams_daily = top_songs_daily['Streams'].astype(str)

        # Use 'max' rank in pd to pull the highest rank in the group & output files
        top_songs_daily['Rank'] = (rank_daily + streams_daily).astype(int).rank(method='max', ascending=False).astype(
            int)
        top_songs_daily = top_songs_daily.sort_values('Rank')
        top_songs_daily.rename(columns={'Track Name': 'TrackName'}, inplace=True)
        top_songs_daily.insert(0, 'TrackID', range(0, 0 + len(top_songs_daily)))

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
            if not artists_d['items']:
                artist_genres_daily.append('')
            else:
                artist_genres_daily.append(artists_d['items'][0]['genres'])

        top_songs_daily['Artist_Genres'] = artist_genres_daily

        top_songs_daily.to_csv(country_daily)

    for country_weekly in weekly:
        # Read input files
        top_songs_weekly = pd.read_csv(country_weekly,
                                       skiprows=range(0, 1))

        # Counting Artist based off number of tracks
        artist_count_weekly = top_songs_weekly.Artist.value_counts()
        artist_count_weekly = artist_count_weekly.to_dict()
        top_songs_weekly['Appears'] = top_songs_weekly.Artist.map(artist_count_weekly)
        top_songs_weekly.sort_values(['Appears'], inplace=True, ascending=False)

        # Creating string combination for amount of times Artist showed up and number of streams
        rank_weekly = top_songs_weekly['Appears'].astype(str)
        streams_weekly = top_songs_weekly['Streams'].astype(str)

        # Use 'max' rank in pd to pull the highest rank in the group & output files
        top_songs_weekly['Rank'] = (rank_weekly + streams_weekly).astype(int).rank(method='max',
                                                                                   ascending=False).astype(int)
        top_songs_weekly = top_songs_weekly.sort_values('Rank')
        top_songs_weekly.rename(columns={'Track Name': 'TrackName'}, inplace=True)
        top_songs_weekly.insert(0, 'TrackID', range(0, 0 + len(top_songs_weekly)))

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
            if not artists_w['items']:
                artist_genres_weekly.append('')
            else:
                artist_genres_weekly.append(artists_w['items'][0]['genres'])

        top_songs_weekly['Artist_Genres'] = artist_genres_weekly

        top_songs_weekly.to_csv(country_weekly)
