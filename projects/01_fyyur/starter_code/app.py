#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import ( 
  Flask, 
  render_template, 
  request, 
  Response, 
  flash, 
  redirect, 
  url_for)
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
from models import * 

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)

# TODO: connect to a local postgresql database //DONE
migrate = Migrate(app, db)


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
  venues = Venue.query.order_by(desc(Venue.created_date)).limit(10).all()
  artists = Artist.query.order_by(desc(Artist.created_date)).limit(10).all()
  return render_template('pages/home.html', venues=venues, artists=artists)


#  Venues
#  ----------------------------------------------------------------
@app.route('/venues')
def venues():
  # TODO: replace with real venues data. //DONE
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  #FIRST WE WILL LIST THE VENUE BASED ON CITY AND STATE 
  cityAndState = Venue.query.order_by(Venue.state, Venue.city)
  data = []
  for c in cityAndState:
    venues = Venue.query.all()
    data.append({"city": c[0],"state": c[1],"venues": venues})
  return render_template('pages/venues.html', areas=data);


@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive. //DONE
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  searchResult = Venue.query.filter(Venue.name.
    ilike("%{}%".format(request.form.get('search_term', '')))).all()
  results={"count": len(searchResult), "data": [] }
  for sr in searchResult:
    results['data'].append({"id": sr.id, "name": sr.name, 
      "num_upcoming_shows": sr.upcoming_shows_count})
  return render_template('pages/search_venues.html', 
    results=results, search_term=request.form.get('search_term', ''))


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id //DONE
  venueByID = Venue.query.get(venue_id)
  past_shows = []
  upcoming_shows = []
  information = []
  showVenue = Venue.shows_v
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
    "seeking_talent": venueByID.seeking_talent,
    "seeking_description": venueByID.seeking_description,
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
  form = VenueForm(request.form)
  try:
    addVenue = Venue(
      name = form.name,
      city = form.city,
      state = form.state,
      address = form.address,
      phone = form.phone,
      image_link = form.image_link,
      facebook_link = form.facebook_link,
      genres = form.genres,
      websit_link = form.websit_link,
      seeking_talent = form.seeking_talent,
      seeking_description = form.seeking_description)
    db.session.add(addVenue)
    db.session.commit()
    # on successful db insert, flash success //DONE
    flash('Venue ' + request.form['name'] + ' was successfully listed!')
  except ValueError as e:
    print(e)
    db.session.rollback()
    # TODO: on unsuccessful db insert, flash an error instead. //DONE
    # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
    flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed.')
  finally:
    db.session.close()
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
    flash('An error occurred. Venue ' + 
      deleteVenueName + ' could not be deleted.')
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
  searchResult = Artist.query.filter(Artist.name.
    ilike("%{}%".format(request.form.get('search_term', '')))).all()
  results={"count": len(searchResult), "data": [] }
  for sr in searchResult:
    results['data'].append({"id": sr.id, "name": sr.name, 
      "num_upcoming_shows": sr.upcoming_shows_count})
  return render_template('pages/search_artists.html', 
    results=results, search_term=request.form.get('search_term', '')) 
  

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
    "seeking_venue": artistByID.seeking_venue,
    "seeking_description": artistByID.seeking_description,
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
    "seeking_venue": artistUpdate.seeking_venue,
    "seeking_description": artistUpdate.seeking_description,
    "image_link": artistUpdate.image_link}
  # TODO: populate form with fields from artist with ID <artist_id> //DONE
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing //DONE
  # artist record with ID <artist_id> using the new attributes
  artist = Artist.query.get(artist_id)
  try:
    artist.name = request.form['name'],
    artist.city = request.form['city'],
    artist.state = request.form['state'],
    artist.phone = request.form['phone'],
    artist.genres = request.form['genres'],
    artist.image_link = request.form['image_link'],
    artist.facebook_link = request.form['facebook_link'],
    artist.websit_link = request.form['websit_link'],
    artist.seeking_venue = request.form['seeking_venue'],
    artist.seeking_description = request.form['seeking_description']
    db.session.commit()
    # on successful db UPDATE, flash success //DONE
    flash('Artist ' + artist.name + ' was successfully update!')
  except ValueError as e:
    print(e)
    db.session.rollback()
    # TODO: on unsuccessful db UPDATE, flash an error UPDATE. //DONE
    # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
    flash('An error occurred. Artist ' + artist.name + ' could not be update.')
  finally:
    db.session.close()
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
    "seeking_talent": venueUpdate.seeking_talent,
    "seeking_description": venueUpdate.seeking_description,
    "image_link": venueUpdate.image_link }
  # TODO: populate form with values from venue with ID <venue_id> //DONE
  return render_template('forms/edit_venue.html', form=form, venue=venue)


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing //DONE
  # venue record with ID <venue_id> using the new attributes
  venue = Venue.query.get(venue_id)
  try:
    venue.name = request.form['name'],
    venue.city = request.form['city'],
    venue.state = request.form['state'],
    venue.address = request.form['address'],
    venue.phone = request.form['phone'],
    venue.image_link = request.form['image_link'],
    venue.facebook_link = request.form['facebook_link'],
    venue.genres = request.form['genres'],
    venue.websit_link = request.form['websit_link'],
    venue.seeking_talent = request.form['seeking_talent'],
    venue.seeking_description = request.form['seeking_description']

    db.session.commit()
    # on successful db UPDATE, flash success //DONE
    flash('Artist ' + venue.name + ' was successfully update!')
  except ValueError as e:
    print(e)
    db.session.rollback()
    # TODO: on unsuccessful db UPDATE, flash an error UPDATE. //DONE
    # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
    flash('An error occurred. Artist '+venue.name+' could not be update.')
  finally:
    db.session.close()
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
  form = ArtistForm(request.form)
  try:
    addArtist = Artist(
      name = form.name,
      city = form.city,
      state = form.state,
      phone = form.phone,
      genres = form.genres,
      image_link = form.image_link,
      facebook_link = form.facebook_link,
      websit_link = form.websit_link,
      seeking_venue = form.seeking_venue,
      seeking_description = form.seeking_description)
    db.session.add(addArtist)
    db.session.commit()
    # on successful db insert, flash success //DONE
    flash('Artist ' + request.form['name'] + ' was successfully listed!')
  except ValueError as e:
    print(e)
    db.session.rollback()
    # TODO: on unsuccessful db insert, flash an error instead. //DONE
    # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
    flash('An error occurred. Artist ' + 
      request.form['name'] + ' could not be listed.')
  finally:
      db.session.close()
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
    Artist = Artist.query.join(Show, Show.artist_id==Artist.id).all()
    Venue = Venue.query.join(Show, Show.venue_id==Venue.id).all()
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
  # renders form. do not touch. 
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)


@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead //DONE
  form = ShowForm(request.form)
  try:
    addShow = Show(
    artist_id = form.artist_id,
    venue_id = form.venue_id,
    start_time = form.start_time)
    db.session.add(addShow)
    db.session.commit()
    # on successful db insert, flash success  //DONE
    flash('Show was successfully listed!')
  except ValueError as e:
    print(e)
    db.session.rollback()
    # TODO: on unsuccessful db insert, flash an error instead. //DONE
    # e.g., flash('An error occurred. Show could not be listed.')
    flash('An error occurred. Show could not be listed.')
  finally:
    db.session.close()
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

@app.errorhandler(400)
def not_found_error(error):
    return render_template('errors/400.html'), 400

@app.errorhandler(401)
def not_found_error(error):
    return render_template('errors/401.html'), 401

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(405)
def not_found_error(error):
    return render_template('errors/405.html'), 405

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter(
          '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
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
