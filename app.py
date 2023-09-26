import os

from flask import Flask, render_template, flash, redirect, url_for, request
from requests import post
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, text

from database import load_animes_from_db, load_flask_key, load_anime_from_db, SearchAnime, engine, Session
from templates.models.anime import Animes

# Create the Flask Application
app = Flask(__name__)

# Add a database and secret key
# Adding ssl certs
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('db_key')
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    "connect_args": {
        "ssl": {
            "ssl_ca": "/etc/ssl/cert.pem"
        }
    }
}
app.secret_key = load_flask_key()

# Start up the database
db = SQLAlchemy(app)

# Run it once and store all data globally so the application can use it
ANIMELIST = load_animes_from_db()


# Pass data to Navbar
@app.context_processor
def base():
    form = SearchAnime()
    return dict(form=form)


@app.route("/")
def anime_finder_home():
    return render_template('views/home.html',
                           animes=ANIMELIST[0:12],
                           company_name='AnimeFinder')


@app.route("/about")
def about_view():
    return render_template('views/about.html',
                           company_name='AnimeFinder')


@app.route("/all")
def all_anime():
    return render_template('views/all.html',
                           animes=ANIMELIST[5:25],
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


# The search function
@app.route("/search", methods=["POST"])
def anime_search():
    form = SearchAnime()
    posts = db.session.query(Animes)
    page = request.args.get('page', 1, type=int)
    if form.validate_on_submit():
        post.searched = form.searched.data
        posts = posts.filter(Animes.a_name.like('%' + post.searched + '%'))
        animes_found = posts.order_by(Animes.a_name).all()
        ANIME_DB = []
        for row in animes_found:
            ANIME_DB.append(row.__dict__)
        # If nothing was found
        if len(animes_found) == 0:
            flash('Sorry, nothing was found. Try searching for something else')
            return redirect(url_for('anime_finder_home'))
        # Otherwise return what we found
        return render_template("views/search.html", form=form,
                               searched=post.searched,
                               animes=ANIME_DB,
                               animes_pages=posts)


if __name__ == "__main__":
    # dev_context = ('local.crt', 'local.key')  # certificate and key files
    # prod_certs = ('cert.pem', 'key.pem')
    app.run(host='127.0.0.1', debug=True)
