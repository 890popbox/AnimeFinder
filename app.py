import os

from flask import Flask, render_template, flash, redirect, url_for, request
from requests import post

from database import load_animes_from_db, load_flask_key, SearchAnime
from models import Animes, db

# Animes in database
anime_count = 24904

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
db.init_app(app)

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
    # Hard coding this in at the moment, will change
    if int(id) < anime_count:
        query = db.session.query(Animes)
        item = query.get(int(id)).__dict__
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
    page = request.args.get('page', 1, type=int)
    if form.validate_on_submit():
        post.searched = form.searched.data
        query = Animes.query.filter(Animes.a_name.like('%' + post.searched + '%')).paginate(page=page, per_page=12)
        ANIME_DB = []
        for row in query:
            print(row)
            ANIME_DB.append(row.__dict__)
        # If nothing was found
        if len(ANIME_DB) == 0:
            flash('Sorry, nothing was found. Try searching for something else')
            return redirect(url_for('anime_finder_home'))
        # Otherwise return what we found
        return render_template("views/search.html", form=form,
                               searched=post.searched,
                               animes=ANIME_DB,
                               animes_pages=query)


if __name__ == "__main__":
    # dev_context = ('local.crt', 'local.key')  # certificate and key files
    # prod_certs = ('cert.pem', 'key.pem')
    app.run(host='127.0.0.1', debug=True)
