# -*- coding: utf-8 -*-

import os
from scripts import spotify_pull

path = os.getcwd()

spotify_pull.topsongs_daily.data_pull(path)
print('Finished spotify data pull')

data_path = os.path.join(path, r'TestData')

spotify_pull.ranking_system.song_rankings(data_path)
print('Finished ranking songs')

spotify_pull.db_funcs.create_db(data_path)
print('Finished creating database')

# db_funcs.update_path(data_path)
# print('Finished updating database')
