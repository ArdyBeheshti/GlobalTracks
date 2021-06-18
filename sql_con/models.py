from sqlalchemy import Boolean, Column, Integer, String, Float, REAL, Text
from sqlalchemy.orm import relationship
import os
import glob
from .database import Base
import re


class Daily(Base):
    current_directory = os.getcwd()
    csv_directory = os.path.join(current_directory, r'Data')
    daily = glob.glob(csv_directory + "/*daily_*.csv")

    for daily_country in daily:
        res = re.findall(r'\w+', daily_country)

        __tablename__ = res[5]

        TrackID = Column(Integer, primary_key=True, index=True)
        Position = Column(Integer)
        TrackName = Column(Text)
        Artist = Column(Text)
        Streams = Column(Integer)
        URL = Column(Float)
        Appears = Column(Integer)
        Rank = Column(Integer)
        SongIDs = Column(Integer)
        Danceability = Column(Float)
        Energy = Column(Float)
        Acousticness = Column(Float)
        Analysis_URL = Column(Text)
        Duration_MS = Column(Integer)
        Spotify_Song_ID = Column(Integer)
        Instrumentalness = Column(Float)
        Key = Column(Integer)
        Liveness = Column(Float)
        Loudness = Column(Float)
        Mode = Column(Integer)
        Speechiness = Column(Float)
        Tempo = Column(Float)
        Time_Signature = Column(Integer)
        Track_Href = Column(Text)
        Search_Type = Column(Text)
        URI = Column(Text)
        Valence = Column(Float)
        Artist_Genres = Column(Text)
        Country = Column(Text)
        Latitude = Column(REAL)
        Longitude = Column(REAL)

        items = relationship("Item", back_populates="owner")

class Weekly(Base):
    current_directory = os.getcwd()
    csv_directory = os.path.join(current_directory, r'Data')
    weekly = glob.glob(csv_directory + "/*weekly_*.csv")

    for weekly_country in weekly:
        res = re.findall(r'\w+', weekly_country)

        __tablename__ = res[5]

        TrackID = Column(Integer, primary_key=True, index=True)
        Position = Column(Integer)
        TrackName = Column(Text)
        Artist = Column(Text)
        Streams = Column(Integer)
        URL = Column(Float)
        Appears = Column(Integer)
        Rank = Column(Integer)
        SongIDs = Column(Integer)
        Danceability = Column(Float)
        Energy = Column(Float)
        Acousticness = Column(Float)
        Analysis_URL = Column(Text)
        Duration_MS = Column(Integer)
        Spotify_Song_ID = Column(Integer)
        Instrumentalness = Column(Float)
        Key = Column(Integer)
        Liveness = Column(Float)
        Loudness = Column(Float)
        Mode = Column(Integer)
        Speechiness = Column(Float)
        Tempo = Column(Float)
        Time_Signature = Column(Integer)
        Track_Href = Column(Text)
        Search_Type = Column(Text)
        URI = Column(Text)
        Valence = Column(Float)
        Artist_Genres = Column(Text)
        Country = Column(Text)
        Latitude = Column(REAL)
        Longitude = Column(REAL)

        items = relationship("Item", back_populates="owner")