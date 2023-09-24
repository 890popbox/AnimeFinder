from flask import Flask, render_template, jsonify, flash, redirect, url_for
from database import load_animes_from_db, load_flask_key, load_anime_from_db

app = Flask(__name__)
app.secret_key = load_flask_key()

# Run it once and store all data globally so the application can use it
ANIMELIST = load_animes_from_db()


@app.route("/")
def anime_finder_home():
    return render_template('views/home.html',
                           animes=ANIMELIST[0:12],
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
    # Searching directly for Anime by the Database ID to avoid too much reads.
    # Also checking for out of bounds, negative does not matter it just scans the database backwards anyway.
    if int(id) < len(ANIMELIST):
        item = load_anime_from_db(int(id))
        print(item)
        return render_template('views/anime.html',
                               anime=item,
                               company_name='AnimeFinder')
    else:
        flash('Sorry, that id does not match an anime. Try searching for one above!')
        return redirect(url_for('anime_finder_home'))


if __name__ == "__main__":
    app.run(host='127.0.0.1', debug=True)
