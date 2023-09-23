from flask import Flask, render_template, jsonify

app = Flask(__name__)

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
'''

ANIMEDUMMYLIST = [
  {
    'id': 1,
    'name': 'Death Note',
    'english_name': 'Death Note',
    'other_name': "notaa death",
    'score': 8,
    'genre': "Comedy",
    'synopsis': "This is where the description will go",
    'type': "Type, TV series, movie, OVA, etc",
    'episodes': "69",
    'aired': "Date aired",
    'premiered': "Date premiered",
    'status': "(e.g., Finished Airing, Currently Airing, etc.).",
    'producers': "The production companies or producers of the anime.",
    'licensors': "(e.g., streaming platforms).",
    'studios': "The animation studios that worked on the anime.",
    'source': "(e.g., manga, light novel, original).",
    'duration': "30 minutes",
    'rating': "The age rating of the anime.",
    'rank': "The rank of the anime based on popularity or other criteria.",
    'popularity': "The popularity rank of the anime.",
    'image': "https://images.alphacoders.com/132/1328054.png"
  },
  {
    'id': 2,
    'name': 'Future Diary',
    'english_name': 'Future Diary',
    'other_name': "mari nikay",
    'score': 8,
    'genre': "Comedy",
    'synopsis': "This is where the description will go",
    'type': "Type, TV series, movie, OVA, etc",
    'episodes': "420",
    'aired': "Date aired",
    'premiered': "Date premiered",
    'status': "(e.g., Finished Airing, Currently Airing, etc.).",
    'producers': "The production companies or producers of the anime.",
    'licensors': "(e.g., streaming platforms).",
    'studios': "The animation studios that worked on the anime.",
    'source': "(e.g., manga, light novel, original).",
    'duration': "30 minutes",
    'rating': "The age rating of the anime.",
    'rank': "The rank of the anime based on popularity or other criteria.",
    'popularity': "The popularity rank of the anime.",
    'image': "https://thepeoplesmovies.com/wp-content/uploads/2016/07/5.jpg"
},
  {
    'id': 3,
    'name': 'Demon Slayer',
    'english_name': 'Demon Slayer',
    'other_name': "slay demons",
    'score': 8,
    'genre': "Comedy",
    'synopsis': "This is where the description will go",
    'type': "Type, TV series, movie, OVA, etc",
    'episodes': "1337",
    'aired': "Date aired",
    'premiered': "Date premiered",
    'status': "(e.g., Finished Airing, Currently Airing, etc.).",
    'producers': "The production companies or producers of the anime.",
    'licensors': "(e.g., streaming platforms).",
    'studios': "The animation studios that worked on the anime.",
    'source': "(e.g., manga, light novel, original).",
    'duration': "30 minutes",
    'rating': "The age rating of the anime.",
    'rank': "The rank of the anime based on popularity or other criteria.",
    'popularity': "The popularity rank of the anime.",
    'image': "https://wallpapers.com/images/hd/demon-slayer-pictures-tsbyd3y88kxirm15.jpg"
}
]

@app.route("/")
def anime_finder():
    return render_template('views/home.html',
                           anime=ANIMEDUMMYLIST,
                           company_name='AnimeFinder')

@app.route("/about")
def about_af():
    return render_template('views/about.html',
                           company_name='AnimeFinder')

if __name__ == "__main__":
  app.run(host='127.0.0.1', debug=True)