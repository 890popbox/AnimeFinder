import pandas as pd
from sqlalchemy import create_engine
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from dotenv import load_dotenv
import os

# Pickle to import the models I created in jupyter notebook
# We are dealing with the CSV file directly and jupyter notebook to easily create and use this model
# In an actual system we will have to actively store information to a live model and pull from a database/userbase.
import pickle

# Load the content-based filtering models I have made, opening the csv of the anime file could work
anime_data = pickle.load(open('data/anime_list.pkl', 'rb'))
tfv_matrix = pickle.load(open('data/matrix.pkl', 'rb'))

from sklearn.metrics.pairwise import sigmoid_kernel

# Compute the sigmoid kernel
sig = sigmoid_kernel(tfv_matrix, tfv_matrix)

# The indices of anime title
indices = pd.Series(anime_data.index, index=anime_data['Name']).drop_duplicates()


def recommend(title, sig=sig):
    # Get the index corresponding to original_title
    idx = indices[title]

    # Get the pairwsie similarity scores
    sig_scores = list(enumerate(sig[idx]))

    # Sort the movies
    sig_scores = sorted(sig_scores, key=lambda x: x[1], reverse=True)

    # Scores of the 10 most similar movies
    sig_scores = sig_scores[1:5]

    # Anime indices, plus one because of the csv file
    anime_indices = [(i[0] + 1) for i in sig_scores]

    return anime_indices


# Nearest Neighbour algorithm
'''
# Creating all the keywords to look for
anime_features = pd.concat([animes['anime_id'], animes['Name'], animes['Genres'].str.get_dummies(sep=',')], axis=1)
anime_features = anime_features.loc[:, "Adventure":].copy()

# Using this for NearestNeighbor algorithm.
from sklearn.preprocessing import MinMaxScaler
from sklearn.neighbors import NearestNeighbors

# Need to transform the models so they can be used properly
anime_feat_scaler = MinMaxScaler()
anime_features_scaled = anime_feat_scaler.fit_transform(anime_features)
knn2 = NearestNeighbors(n_neighbors=11, algorithm='brute', metric='cosine').fit(anime_features_scaled)
all_anime_names = list(animes['Name'])

# Recommending a few animes based off the one we are viewing, collect their IDs
def recommend(anime):
    # Create a list to collect these IDs and perform NearestNeighbour algorithm
    similar_anime_id = []
    query_index = all_anime_names.index(anime)
    distances1, indices1 = knn2.kneighbors(anime_features_scaled[query_index].reshape(1, -1), n_neighbors=11)
    # Collect four IDs of the most similar anime to the given parameter
    for i in range(1, 5):
        similar_anime_id.append(indices1.flatten()[i] + 1)
    return similar_anime_id
'''


# Reading the key from an environment file, could do this to a text file as well and not include it in repo.

def configure():
    load_dotenv()


# Call it before starting up the engine
configure()

# Here is how I connect to a PlanetScale Database using secure ssl certificate.
# May use similar method starting up the server
engine = create_engine(os.getenv('db_key'),
                       connect_args={
                           "ssl": {
                               "ssl_ca": "/etc/ssl/cert.pem"
                           }
                       })


# Function to load our secret flask_key
def load_flask_key():
    return os.getenv('flask_key')


# Class to search for an anime from the database via query.
class SearchAnime(FlaskForm):
    searched = StringField("searched", validators=[DataRequired()])
    submit = SubmitField("submit")

# The model I trained uses only four tags to perform cosine similarity
# (Name, English name, Genre, and Studio) Reason: The names could be slightly different (This helps avoid
# shows that just have common names, leaning the model more towards something relevant) The genre and studio,
# I feel if you like the show you may like shows within that genre or from the same studio. Other keywords and tags
# could potentially be introduced in future models depending on if a user-base was introduced.
# This is simple and leans towards relevant results.
