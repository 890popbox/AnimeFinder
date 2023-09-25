# This class belongs to the table animes, including all the columns we need here
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import declarative_base
Base = declarative_base()


class Animes(Base):
    __tablename__ = 'animes'
    id = Column(Integer, primary_key=True, autoincrement=True)
    anime_id = Column(Integer, primary_key=True)
    a_name = Column(String(150))
    english_name = Column(String(150))
    other_name = Column(String(150))
    score = Column(String(15))
    genre = Column(String(150))
    synopsis = Column(String(5000))
    a_type = Column(String(15))
    episodes = Column(String(15))
    aired = Column(String(45))
    premiered = Column(String(30))
    anime_status = Column(String(30))
    producers = Column(String(500))
    licensors = Column(String(100))
    studios = Column(String(150))
    a_source = Column(String(30))
    duration = Column(String(30))
    rating = Column(String(30))
    a_rank = Column(String(15))
    popularity = Column(Integer)
    favorites = Column(Integer)
    scored_by = Column(String(15))
    members = Column(Integer)
    image = Column(String(100))


# Description of each item below and names adjusted above to fit a database.
'''
anime_id: Unique ID for each anime.
Name: The name of the anime in its original language.
English name: The English name of the anime.
Other name: Native name or title of the anime(can be in Japanese, Chinese or Korean).
Score: The score or rating given to the anime.
Genres: The genres of the anime, separated by commas.
Synopsis: A brief description or summary of the anime's plot.
Type: The type of the anime (e.g., TV series, movie, OVA, etc.).
Episodes: The number of episodes in the anime.
Aired: The dates when the anime was aired.
Premiered: The season and year when the anime premiered.
Status: The status of the anime (e.g., Finished Airing, Currently Airing, etc.).
Producers: The production companies or producers of the anime.
Licensors: The licensors of the anime (e.g., streaming platforms).
Studios: The animation studios that worked on the anime.
Source: The source material of the anime (e.g., manga, light novel, original).
Duration: The duration of each episode.
Rating: The age rating of the anime.
Rank: The rank of the anime based on popularity or other criteria.
Popularity: The popularity rank of the anime.
Image URL: Link to image
'''
