from flask import Flask, render_template, jsonify, flash, redirect, url_for
from database import load_animes_from_db

app = Flask(__name__)

# Run it once and store all data globally so the application can use it
ANIMELIST = load_animes_from_db()


@app.route("/")
def anime_finder_home():
    return render_template('views/home.html',
                           animes=ANIMELIST[1:13],
                           company_name='AnimeFinder')


@app.route("/about")
def about_view():
    return render_template('views/about.html',
                           company_name='AnimeFinder')


@app.route("/anime")
def all_anime():
    return render_template('views/all.html',
                           anime=ANIMELIST[5:25],
                           company_name='AnimeFinder')


@app.route("/anime/<id>")
def anime_view(id):
    for i in range(1, len(ANIMELIST)):
        if (ANIMELIST[i]['anime_id'] == int(id)):
            return render_template('views/anime.html',
                                   anime=ANIMELIST[i],
                                   company_name='AnimeFinder')
    else:
        flash('Sorry, that id does not match an anime. Try searching for one above!')
        return redirect(url_for('anime_finder_home'))


if __name__ == "__main__":
    app.secret_key = 'the random string'
    app.run(host='127.0.0.1', debug=True)
