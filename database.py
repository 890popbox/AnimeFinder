from sqlalchemy import create_engine, text
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from dotenv import load_dotenv
import os

# Pickle to import the models I created in jupyter notebook
# We are dealing with the CSV file directly and jupyter notebook to easily create and use this model
# In an actual system we will have to actively store information to a live model and pull from a database/userbase.
import pickle

# Load the content-based filtering models I have made
a_model = pickle.load(open('data/anime_list.pkl', 'rb'))
similarity = pickle.load(open('data/similarity.pkl', 'rb'))


# Recommending a few animes based off the one we are viewing, collect their IDs
def recommend(anime):
    # In this example we must be viewing a valid anime name that exists in our database.
    index = a_model[a_model['Name'] == anime].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    # Holding the IDs of a few animes with the best cosine similarity.
    # (This means they will be closely related. (See above
    ls = []
    for i in distances[1:5]:
        # print(a_model.iloc[i[0]].Name)
        ls.append(i[0] + 1)  # The first column (0) is not relevant to our search, This is the title/name/etc.
    return ls


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
