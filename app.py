import os

from flask import Flask, render_template, flash, redirect, url_for, request
from requests import post

from database import load_flask_key, SearchAnime, recommend
from models import Animes, db

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

# Animes in database, This is hardcoded to avoid scanning the table each time for now.
anime_count = 24904

# Dynamic way to get the total items in a database, This runs once at the beginning of the application stateup
'''
with app.app_context():
    anime_count = Animes.query.count()
    print(anime_count)
'''

# Pass data to Navbar
@app.context_processor
def base():
    form = SearchAnime()
    return dict(form=form)


@app.route("/")
def anime_finder_home():
    ANIMELIST = Animes.query.filter(Animes.score != "UNKNOWN").order_by(Animes.popularity.asc()).limit(12)
    return render_template('views/home.html',
                           animes=ANIMELIST,
                           company_name='AnimeFinder')


@app.route("/about")
def about_view():
    return render_template('views/about.html',
                           company_name='AnimeFinder')


# The initial all route
@app.route("/all")
def all_anime():
    return redirect(url_for('all_anime_page', page_num=1))


# The all route page we are on
@app.route("/all/page=<page_num>", methods=["GET", "POST"])
def all_anime_page(page_num):
    page = request.args.get('page', page_num, type=int)
    query = Animes.query.order_by(Animes.a_name).paginate(page=int(page), per_page=16)
    return render_template('views/all.html',
                           company_name='AnimeFinder',
                           animes_page=query)


@app.route("/anime/<id>")
def anime_view(id):
    # Searching directly for Anime by the Database ID to avoid too much reads.
    # Also checking for out of bounds, negative does not matter it just scans the database backwards anyway.
    # Hard coding this in at the moment, will change
    if int(id) < anime_count:
        item = db.session.get(Animes, int(id))

        #recommended_id = recommend(item.a_name)
        recommended_animes = []

        '''
        for item in recommended_id:
            recommended_animes.append(Animes.query.get(int(id)))
        '''

        return render_template('views/anime.html',
                               anime=item,
                               recommend=recommended_animes,
                               company_name='AnimeFinder')
    else:
        flash('Sorry, that id does not match an anime. Try searching for one above!')
        return redirect(url_for('anime_finder_home'))


# The initial search route to validate the search
@app.route("/search/", methods=["GET", "POST"])
def validate_search():
    form = SearchAnime()
    if form.validate_on_submit():
        post.searched = form.searched.data
        phrase = post.searched
        return redirect(url_for('anime_search', phrase=phrase, page_num=1))
    else:
        flash('Sorry, An error occurred during your search, please try again.')
        return redirect(url_for('anime_finder_home'))


# The anime search function with defaults
@app.route("/search/<phrase>/page=<page_num>", methods=["GET", "POST"])
def anime_search(phrase, page_num):
    form = SearchAnime()
    page = request.args.get('page', page_num, type=int)
    query = Animes.query.filter(Animes.a_name.like('%' + phrase + '%')).filter(Animes.score != "UNKNOWN")\
        .order_by(Animes.popularity.asc()).paginate(page=int(page), per_page=12)

    # If nothing was found
    if len(query.items) == 0:
        flash('Sorry, nothing was found. Try searching for something else')
        return redirect(url_for('anime_finder_home'))
        # Otherwise return what we found
    return render_template("views/search.html", form=form,
                           searched=phrase,
                           animes_page=query)


if __name__ == "__main__":
    # dev_context = ('local.crt', 'local.key')  # certificate and key files
    # prod_certs = ('cert.pem', 'key.pem')
    app.run(host='127.0.0.1', debug=True)
