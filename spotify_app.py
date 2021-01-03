# -*- coding: utf-8 -*-
"""
Created on Sun Dec 27 13:41:56 2020

@author: ardyb
"""

import os
import topsongs_daily
import ranking_system
import create_db
# import get_song_info

path = os.chdir(r'D:\Diddly\Python\Stream')

topsongs_daily.DataPull(path)
print('Finished spotify data pull')

ranking_system.SongRankings(path)
print('Finished ranking songs')

create_db.CreateDB(path)
print('Finished creating database')
