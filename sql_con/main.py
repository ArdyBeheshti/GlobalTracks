from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from safrs import SAFRSBase, SAFRSAPI

db = SQLAlchemy()


class Daily(SAFRSBase, db.Model):
    __tablename__ = "us_top_200_daily_20210309"

    TrackID = db.Column(db.Integer, primary_key=True)
    Position = db.Column(db.Integer)
    TrackName = db.Column(db.Text)
    Artist = db.Column(db.Text)
    Streams = db.Column(db.Integer)
    URL = db.Column(db.Float)
    Appears = db.Column(db.Integer)
    Rank = db.Column(db.Integer)
    SongIDs = db.Column(db.Integer)
    Danceability = db.Column(db.Float)
    Energy = db.Column(db.Float)
    Acousticness = db.Column(db.Float)
    Analysis_URL = db.Column(db.Text)
    Duration_MS = db.Column(db.Integer)
    Spotify_Song_ID = db.Column(db.Integer)
    Instrumentalness = db.Column(db.Float)
    Key = db.Column(db.Integer)
    Liveness = db.Column(db.Float)
    Loudness = db.Column(db.Float)
    Mode = db.Column(db.Integer)
    Speechiness = db.Column(db.Float)
    Tempo = db.Column(db.Float)
    Time_Signature = db.Column(db.Integer)
    Track_Href = db.Column(db.Text)
    Search_Type = db.Column(db.Text)
    URI = db.Column(db.Text)
    Valence = db.Column(db.Float)
    Artist_Genres = db.Column(db.Text)
    Country = db.Column(db.Text)
    Latitude = db.Column(db.REAL)
    Longitude = db.Column(db.REAL)


class Weekly(SAFRSBase, db.Model):
    __tablename__ = "us_top_200_weekly_20210309"

    TrackID = db.Column(db.Integer, primary_key=True)
    Position = db.Column(db.Integer)
    TrackName = db.Column(db.Text)
    Artist = db.Column(db.Text)
    Streams = db.Column(db.Integer)
    URL = db.Column(db.Float)
    Appears = db.Column(db.Integer)
    Rank = db.Column(db.Integer)
    SongIDs = db.Column(db.Integer)
    Danceability = db.Column(db.Float)
    Energy = db.Column(db.Float)
    Acousticness = db.Column(db.Float)
    Analysis_URL = db.Column(db.Text)
    Duration_MS = db.Column(db.Integer)
    Spotify_Song_ID = db.Column(db.Integer)
    Instrumentalness = db.Column(db.Float)
    Key = db.Column(db.Integer)
    Liveness = db.Column(db.Float)
    Loudness = db.Column(db.Float)
    Mode = db.Column(db.Integer)
    Speechiness = db.Column(db.Float)
    Tempo = db.Column(db.Float)
    Time_Signature = db.Column(db.Integer)
    Track_Href = db.Column(db.Text)
    Search_Type = db.Column(db.Text)
    URI = db.Column(db.Text)
    Valence = db.Column(db.Float)
    Artist_Genres = db.Column(db.Text)
    Country = db.Column(db.Text)
    Latitude = db.Column(db.REAL)
    Longitude = db.Column(db.REAL)


def create_api(app, HOST="localhost", PORT=5000, API_PREFIX=""):
    api = SAFRSAPI(app, host=HOST, port=PORT, prefix=API_PREFIX)
    api.expose_object(Daily)
    api.expose_object(Weekly)
    print("Starting API: http://{}:{}/{}".format(HOST, PORT, API_PREFIX))


def create_app(config_filename=None, host="localhost"):
    app = Flask("demo_app")
    app.config.update(SQLALCHEMY_DATABASE_URI="sqlite:////Diddly/Python/GlobalTracks/sql_con/Spotify_Rankings.db")
    db.init_app(app)
    with app.app_context():
        db.create_all()
        create_api(app, host)
    return app


host = "localhost"
app = create_app(host=host)

if __name__ == "__main__":
    app.run(host=host)