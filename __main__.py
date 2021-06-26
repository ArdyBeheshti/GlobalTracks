import os
from scripts.spotify_pull import SpotifyPull

path = os.getcwd()
data_path = os.path.join(path, r'TestData')

SpotifyPull.data_pull(path)
SpotifyPull.song_rankings(data_path)
SpotifyPull.geocode(data_path)
# SpotifyPull.create_db(data_path)