import copy

from flask import Flask, render_template, jsonify, flash, redirect, url_for
from templates.models.anime import anime_model
import csv

app = Flask(__name__)

ANIMEDUMMYLIST = []

with open("static/anime-dataset-2023.csv", encoding="utf8") as csv_file:
    Anime_Data = csv.reader(csv_file, delimiter=",")
    Anime_Data = list(Anime_Data)

print(anime_model)

for data in Anime_Data:
    item = copy.deepcopy(anime_model)
    item['anime_id'], item['name'], item['english_name'] = data[0], data[1], data[2]
    item['other_name'], item['score'], item['genres'] = data[3], data[4], data[5]
    item['synopsis'], item['type'], item['episodes'] = data[6], data[7], data[8]
    item['aired'], item['premiered'], item['status'] = data[9], data[10], data[11]
    item['producers'], item['licensors'], item['studios'] = data[12], data[13], data[14]
    item['source'], item['duration'], item['rating'] = data[15], data[16], data[17]
    item['rank'], item['popularity'], item['favorites'] = data[18], data[19], data[20]
    item['scored_by'], item['members'], item['image'] = data[21], data[22], data[23]
    ANIMEDUMMYLIST.append(item)

print(ANIMEDUMMYLIST)

@app.route("/")
def anime_finder_home():
    return render_template('views/home.html',
                           animes=ANIMEDUMMYLIST[1:13],
                           company_name='AnimeFinder')


@app.route("/about")
def about_view():
    return render_template('views/about.html',
                           company_name='AnimeFinder')


@app.route("/anime")
def all_anime():
    return render_template('views/all.html',
                           anime=ANIMEDUMMYLIST[5:25],
                           company_name='AnimeFinder')


@app.route("/anime/<id>")
def anime_view(id):
    for i in range(1, len(ANIMEDUMMYLIST)):
        if(ANIMEDUMMYLIST[i]['anime_id']==id):
            return render_template('views/anime.html',
                                   anime=ANIMEDUMMYLIST[i],
                                   company_name='AnimeFinder')
    else:
        flash('Sorry, that id does not match an anime. Try searching for one above!')
        return redirect(url_for('anime_finder_home'))

if __name__ == "__main__":
    app.secret_key = 'the random string'
    app.run(host='127.0.0.1', debug=True)
