from sqlalchemy import create_engine, text
from flask_wtf import FlaskForm
from sqlalchemy.orm import sessionmaker
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
# Integer, Column, String
# from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

# Data analysis process
import numpy as np  # To perform linear algebra
import pandas as pd  # For data processing
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# Creating Anime dataframe to be used

anime_df = pd.read_csv("data/anime-dataset-2023.csv")
anime_df = anime_df[['anime_id', 'Name', 'English name', 'Genres', 'Studios']]
anime_df['tags'] = (anime_df['Name'] + ' ') + (anime_df['English name'] + ' ') + anime_df['Genres'] + anime_df['Studios']


# Recommending a few animes based off the one we are viewing, collect their IDs

def recommend(anime):
    cv = CountVectorizer(max_features=5000, stop_words='english')  # Create a vector to be used for cosine similarity

    vector = cv.fit_transform(anime_df['tags']).toarray()  # Transform the tags to be used as a vector
    similarity = cosine_similarity(vector)
    index = anime_df[anime_df['Name'] == anime].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    ls = []
    for i in distances[1:10]:
        ls.append(anime_df.iloc[i[0]].anime_id)
    return ls

# Reading the key from an environment file, could do this to a text file as well and not include it in repo.

# Function to configure the project potentially
from models import Animes


def configure():
    load_dotenv()


# Call it before starting up the engine
configure()

# Here is how I connect to a PlanetScale Database using secure ssl certificate.
engine = create_engine(os.getenv('db_key'),
                       connect_args={
                           "ssl": {
                               "ssl_ca": "/etc/ssl/cert.pem"
                           }
                       })


# Function to load all anime from the database.
def load_animes_from_db():
    with engine.connect() as conn:
        # Limiting to avoid too much reads in my database for development purposes
        result = conn.execute(text("select * from animes limit 50;")
                              )
        ANIME_DB = []
        for row in result.all():
            ANIME_DB.append(row)
        return ANIME_DB


# Function to load a specific anime from the database using its ID.
def load_anime_from_db(id):
    with engine.connect() as conn:
        result = conn.execute(
            text(f"select * from animes where id = {id} limit 50;")
        )
        rows = result.all()
        if len(rows) == 0:
            return None
        else:
            return rows[0]


# Function to load our secret flask_key
def load_flask_key():
    return os.getenv('flask_key')


# Class to search for an anime from the database via query.
class SearchAnime(FlaskForm):
    searched = StringField("searched", validators=[DataRequired()])
    submit = SubmitField("submit")


# Function to load anime searched for
def search_anime_from_db(search):
    with engine.connect() as conn:
        result = conn.execute(
            text(f"select * from animes where id = {id}  limit 50;")
        )


# Create a session to the engine, and a base class to use
Session = sessionmaker(engine)
# Base = declarative_base()


# This class belongs to the table animes, including all the columns we need here
# This is in the template/models folder.
# Anime = Animes


# Reading data from a csv file, this contains about 25,000 different animes
'''
# Creating a list to hold all the anime entries
ANIMEDUMMYLIST = []

with open("anime-dataset-2023.csv", encoding="utf8") as csv_file:
    Anime_Data = csv.reader(csv_file, delimiter=",")
    Anime_Data = list(Anime_Data)
'''

# The first row will be the description, so we will avoid that and go through the end, making a model each time.
# This was the initial seed of the database and does not need to be ran more than once.

'''
for data in Anime_Data[1:-1]:
    print(data)
    item = Anime(anime_id=int(data[0]),
                 a_name=data[1],
                 english_name=data[2],
                 other_name=data[3],
                 score=data[4],
                 genre=data[5],
                 synopsis=data[6],
                 a_type=data[7],
                 episodes=data[8],
                 aired=data[9],
                 premiered=data[10],
                 anime_status=data[11],
                 producers=data[12],
                 licensors=data[13],
                 studios=data[14],
                 a_source=data[15],
                 duration=data[16],
                 rating=data[17],
                 a_rank=data[18],
                 popularity=int(data[19]),
                 favorites=int(data[20]),
                 scored_by=data[21],
                 members=int(data[22]),
                 image=data[23]
                 )
    ANIMEDUMMYLIST.append(item)
'''

# Create the session, and add_all instead of add because its a list, commit changes and all data has been inserted.
'''
session = Session()
session.add_all(ANIMEDUMMYLIST)
session.commit()
'''
