#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
#app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:postgres@localhost:5432/fyyur_pro"
db = SQLAlchemy(app)

# TODO: connect to a local postgresql database //DONE
migrate = Migrate(app, db)

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    # TODO: implement any missing fields, as a database migration using Flask-Migrate //DONE
    genres = db.Column(db.String(120))
    websit_link = db.Column(db.String(120))
    talent = db.Column(db.Boolean, default=False)
    description = db.Column(db.String(1000))
    upcoming_shows_count = db.Column(db.Integer, default=0)
    past_shows_count = db.Column(db.Integer, default=0)
    # PARENT CLASS
    shows_v = db.relationship('Show', backref='artist', cascade='delete, merge, save-update')

    def __init__(self, name, city, state, address, phone, image_link, facebook_link, genres, websit_link, description, talent=False, upcoming_shows_count=0, past_shows_count=0):
      self.name = name
      self.city = city
      self.state = state
      self.address = address
      self.phone = phone
      self.image_link = image_link
      self.facebook_link = facebook_link
      self.genres = genres
      self.websit_link = websit_link
      self.talent = talent
      self.description = description
      self.upcoming_shows_count = upcoming_shows_count
      self.past_shows_count = past_shows_count


class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    # TODO: implement any missing fields, as a database migration using Flask-Migrate //DONE
    websit_link = db.Column(db.String(120))
    venues_Art = db.Column(db.Boolean, default=False)
    description = db.Column(db.String(1000))
    upcoming_shows_count = db.Column(db.Integer, default=0)
    past_shows_count = db.Column(db.Integer, default=0)
    # PARENT CLASS
    shows_a = db.relationship('Show', backref='artist', cascade='delete, merge, save-update')

    def __init__(self, name, city, state, phone, genres, image_link, facebook_link,  websit_link, description, venues_Art=False, upcoming_shows_count=0, past_shows_count=0):
      self.name = name
      self.city = city
      self.state = state
      self.phone = phone
      self.genres = genres
      self.image_link = image_link
      self.facebook_link = facebook_link
      self.websit_link = websit_link
      self.venues_Art = venues_Art
      self.description = description
      self.upcoming_shows_count = upcoming_shows_count
      self.past_shows_count = past_shows_count


# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration. //DONE
class Show(db.Model):
    __tablename__ = 'Show'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), nullable=False) # CHILD CLASS
    venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable=False) # CHILD CLASS
    start_time = db.Column(db.DateTime, nullable=False)
    upcoming = db.Column(db.Boolean, nullable=False, default=True)



# TO CREATE THE DATABASE AND TABLES 
db.create_all()
#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime


#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#
@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # TODO: replace with real venues data. //DONE
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  cityAndState = db.session.query(Venue.state, Venue.city).group_by(Venue.state, Venue.city).all()
  #cityAndState = Venue.query.group_by(Venue.state, Venue.city).all()
  data = []
  for c in cityAndState:
    venues = db.session.query(Venue.id,Venue.name,
      Venue.upcoming_shows_count).filter(Venue.city==c[0],Venue.state==c[1]).all()
    data.append({
        "city": c[0],
        "state": c[1],
        "venues": []})
    for v in venues:
      data[-1]["venues"].append({
              "id": v[0],
              "name": v[1],
              "num_upcoming_shows":v[2]})
  return render_template('pages/venues.html', areas=data);




@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive. //DONE
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  searchResult = Venue.query.filter(Venue.name.ilike("%", request.form['search_term'] ,"%")).all()
  response={
    "count": len(searchResult),
    "data": [] }
  for sr in searchResult:
    response['data'].append({
         "id": sr.id,
         "name": sr.name,
         "num_upcoming_shows": sr.upcoming_shows_count})
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id //DONE
  venueByID = Venue.query.get(venue_id)
  past_shows = []
  upcoming_shows = []
  information = []
  showVenue = Venue.shows
  for s in showVenue:
    information = {
      "artist_id": s.artist_id,
      "artist_name": s.Artist.name,
      "artist_image_link": s.Artist.image_link,
      "start_time": s.start_time}
    if(s.upcoming):
      upcoming_shows.append(information)
    else:
      past_shows.append(information)

  dataToShow={
    "id": venueByID.id,
    "name": venueByID.name,
    "genres": venueByID.genres,
    "address": venueByID.address,
    "city": venueByID.city,
    "state": venueByID.state,
    "phone": venueByID.phone,
    "website": venueByID.websit_link,
    "facebook_link": venueByID.facebook_link,
    "talent": venueByID.talent,
    "description": venueByID.description,
    "image_link": venueByID.image_link,
    "past_shows": past_shows,
    "upcoming_shows": upcoming_shows,
    "past_shows_count": len(past_shows),
    "upcoming_shows_count": len(upcoming_shows) }
  return render_template('pages/show_venue.html', venue=dataToShow)


#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead //DONE
  # TODO: modify data to be the data object returned from db insertion //DONE
  # CREATE AN OBJECT FROM THE CLASS
  addVenue = Venue(
    name = request.form['name'],
    city = request.form['city'],
    state = request.form['state'],
    address = request.form['address'],
    phone = request.form['phone'],
    image_link = request.form['image_link'],
    facebook_link = request.form['facebook_link'],
    genres = request.form['genres'],
    websit_link = request.form['websit_link'],
    talent = request.form['talent'],
    description = request.form['description'])
  try:
    db.session.add(addVenue)
    db.session.commit()
    # on successful db insert, flash success //DONE
    flash('Venue ' + request.form['name'] + ' was successfully listed!')
  except:
    # TODO: on unsuccessful db insert, flash an error instead. //DONE
    # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
    flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')



@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using //DONE
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  deleteVenue = Venue.query.get(venue_id)
  deleteVenueName = deleteVenue.name

  if deleteVenue:
    db.session.delete(deleted_venue)
    db.session.commit()
    flash('Venue ' + deleteVenueName + ' was successfully deleted!')
  else:
    db.session.rollback()
    flash('An error occurred. Venue ' + deleteVenueName + ' could not be deleted.')
  db.session.close()

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return None

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database //DONE
  data = []
  artists = Artist.query.all()
  for a in artists:
    data.append({
      "id": a.id,
      "name": a.name
      })
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive. //DONE
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  searchResult = Artist.query.filter(Artist.name.ilike("%", request.form['search_term'] ,"%")).all()
  response={
    "count": len(searchResult),
    "data": [] }
  for sr in searchResult:
    response['data'].append({
         "id": sr.id,
         "name": sr.name,
         "num_upcoming_shows": sr.upcoming_shows_count,
       })
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))  
  

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given artist_id 
  # TODO: replace with real artist data from the artist table, using artist_id //DONE 

  artistByID = Artist.query.get(artist_id)
  past_shows = []
  upcoming_shows = []
  information = []
  showArtist = Artist.shows
  for s in showArtist:
    information = {
      "venue_id": s.venue_id,
      "venue_name": s.Venue.name,
      "venue_image_link":s.Venue.image_link,
      "start_time": s.start_time}
    if(s.upcoming):
      upcoming_shows.append(information)
    else:
      past_shows.append(information)

  dataToShow={
    "id": artistByID.id,
    "name": artistByID.name,
    "genres": artistByID.genres,
    "city": artistByID.city,
    "state": artistByID.state,
    "phone": artistByID.phone,
    "websit_link": artistByID.websit_link,
    "facebook_link": artistByID.facebook_link,
    "venues_Art": artistByID.venues_Art,
    "description": artistByID.description,
    "image_link": artistByID.image_link,
    "past_shows": past_shows,
    "upcoming_shows": upcoming_shows,
    "past_shows_count": len(past_shows),
    "upcoming_shows_count": len(upcoming_shows)}
  return render_template('pages/show_artist.html', artist=dataToShow)



#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artistUpdate = Artist.query.get(artist_id).all()
  artist={
    "id": artistUpdate.id,
    "name": artistUpdate.name,
    "genres": artistUpdate.genres,
    "city": artistUpdate.city,
    "state": artistUpdate.state,
    "phone": artistUpdate.phone,
    "websit_link": artistUpdate.websit_link,
    "facebook_link": artistUpdate.facebook_link,
    "venues_Art": artistUpdate.venues_Art,
    "description": artistUpdate.description,
    "image_link": artistUpdate.image_link}
  # TODO: populate form with fields from artist with ID <artist_id> //DONE
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing //DONE
  # artist record with ID <artist_id> using the new attributes
  artist = Artist.query.get(artist_id)

  artist.name = request.form['name'],
  artist.city = request.form['city'],
  artist.state = request.form['state'],
  artist.phone = request.form['phone'],
  artist.genres = request.form['genres'],
  artist.image_link = request.form['image_link'],
  artist.facebook_link = request.form['facebook_link'],
  artist.websit_link = request.form['websit_link'],
  artist.venues_Art = request.form['venues_Art'],
  artist.description = request.form['description']

  try:
    db.session.commit()
    # on successful db UPDATE, flash success //DONE
    flash('Artist ' + artist.name + ' was successfully update!')
  except:
    # TODO: on unsuccessful db UPDATE, flash an error UPDATE. //DONE
    # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
    flash('An error occurred. Artist ' + artist.name + ' could not be update.')
  return redirect(url_for('show_artist', artist_id=artist_id))


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venueUpdate = Venue.query.get(venue_id).all()
  venue={
    "id": venueUpdate.id,
    "name": venueUpdate.name,
    "genres": venueUpdate.genres,
    "address": venueUpdate.address,
    "city": venueUpdate.city,
    "state": venueUpdate.state,
    "phone": venueUpdate.phone,
    "website": venueUpdate.websit_link,
    "facebook_link": venueUpdate.facebook_link,
    "talent": venueUpdate.talent,
    "description": venueUpdate.description,
    "image_link": venueUpdate.image_link }
  # TODO: populate form with values from venue with ID <venue_id> //DONE
  return render_template('forms/edit_venue.html', form=form, venue=venue)


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing //DONE
  # venue record with ID <venue_id> using the new attributes
  venue = Venue.query.get(venue_id)

  venue.name = request.form['name'],
  venue.city = request.form['city'],
  venue.state = request.form['state'],
  venue.address = request.form['address'],
  venue.phone = request.form['phone'],
  venue.image_link = request.form['image_link'],
  venue.facebook_link = request.form['facebook_link'],
  venue.genres = request.form['genres'],
  venue.websit_link = request.form['websit_link'],
  venue.talent = request.form['talent'],
  venue.description = request.form['description']

  try:
    db.session.commit()
    # on successful db UPDATE, flash success //DONE
    flash('Artist ' + venue.name + ' was successfully update!')
  except:
    # TODO: on unsuccessful db UPDATE, flash an error UPDATE. //DONE
    # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
    flash('An error occurred. Artist ' + venue.name + ' could not be update.')
  return redirect(url_for('show_venue', venue_id=venue_id))



#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead //DONE
  # TODO: modify data to be the data object returned from db insertion //DONE
  addArtist = Artist(
    name = request.form['name'],
    city = request.form['city'],
    state = request.form['state'],
    phone = request.form['phone'],
    genres = request.form['genres'],
    image_link = request.form['image_link'],
    facebook_link = request.form['facebook_link'],
    websit_link = request.form['websit_link'],
    venues_Art = request.form['venues_Art'],
    description = request.form['description'])
  try:
    db.session.add(addArtist)
    db.session.commit()
    # on successful db insert, flash success //DONE
    flash('Artist ' + request.form['name'] + ' was successfully listed!')
  except:
    # TODO: on unsuccessful db insert, flash an error instead. //DONE
    # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
    flash('An error occurred. Artist ' + request.form['name'] + ' could not be listed.')
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows //DONE
  # TODO: replace with real venues data. //DONE
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  data = []
  Shows = Show.query.all()
  for s in Shows:
    data.append({
      "venue_id": s.Venue.id,
      "venue_name": s.Venue.name,
      "artist_id": s.Artist.id,
      "artist_name": s.Artist.name,
      "artist_image_link": s.Artist.image_link,
      "start_time": s.start_time
      })
  return render_template('pages/shows.html', shows=data)


@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.  //DONE :)
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)


@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead //DONE

  addShow = Show(
  artist_id = request.form['artist_id'],
  venue_id = request.form['venue_id'],
  start_time = request.form['start_time'],)

  try:
    db.session.add(addShow)
    db.session.commit()
    # on successful db insert, flash success  //DONE
    flash('Show was successfully listed!')
  except:
    # TODO: on unsuccessful db insert, flash an error instead. //DONE
    # e.g., flash('An error occurred. Show could not be listed.')
    flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#


# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
