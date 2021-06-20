# -*- coding: utf-8 -*-
"""
Created on Sun Dec 27 13:41:56 2020

@author: ardyb
"""

import os
import topsongs_daily
import ranking_system
import db_funcs

path = os.getcwd()
data_path = os.path.join(path, r'TestData')

topsongs_daily.data_pull(path)
print('Finished spotify data pull')

ranking_system.song_rankings(data_path)
print('Finished ranking songs')

# db_funcs.create_db(data_path)
# print('Finished creating database')

db_funcs.update_path(data_path)
print('Finished updating database')
