from flask_sqlalchemy import SQLAlchemy
#from flask_migrate import Migrate
from flask import Flask
from flask_moment import Moment
from flask_migrate import Migrate

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)

# TODO: connect to a local postgresql database //DONE
migrate = Migrate(app, db)

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'venues'

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
    seeking_talent = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String(1000))
    upcoming_shows_count = db.Column(db.Integer, default=0)
    past_shows_count = db.Column(db.Integer, default=0)
    # PARENT CLASS
    shows_v = db.relationship('Show', backref='Venue', 
        cascade='delete, merge, save-update')

    def __init__(self, name, city, state, address, phone, image_link, 
        facebook_link, genres, websit_link, seeking_description, 
        seeking_talent=False, upcoming_shows_count=0, past_shows_count=0):
      self.name = name
      self.city = city
      self.state = state
      self.address = address
      self.phone = phone
      self.image_link = image_link
      self.facebook_link = facebook_link
      self.genres = genres
      self.websit_link = websit_link
      self.seeking_talent = seeking_talent
      self.seeking_description = seeking_description
      self.upcoming_shows_count = upcoming_shows_count
      self.past_shows_count = past_shows_count


class Artist(db.Model):
    __tablename__ = 'artists'

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
    seeking_venue = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String(1000))
    upcoming_shows_count = db.Column(db.Integer, default=0)
    past_shows_count = db.Column(db.Integer, default=0)
    # PARENT CLASS
    shows_a = db.relationship('Show', backref='Artist', 
        cascade='delete, merge, save-update')

    def __init__(self, name, city, state, phone, genres, image_link, 
        facebook_link,  websit_link, seeking_description, seeking_venue=False, 
        upcoming_shows_count=0, past_shows_count=0):
      self.name = name
      self.city = city
      self.state = state
      self.phone = phone
      self.genres = genres
      self.image_link = image_link
      self.facebook_link = facebook_link
      self.websit_link = websit_link
      self.seeking_venue = seeking_venue
      self.seeking_description = seeking_description
      self.upcoming_shows_count = upcoming_shows_count
      self.past_shows_count = past_shows_count


# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration. //DONE
class Show(db.Model):
    __tablename__ = 'shows'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), nullable=False) # CHILD CLASS
    venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable=False) # CHILD CLASS
    start_time = db.Column(db.DateTime, nullable=False)
    upcoming = db.Column(db.Boolean, nullable=False, default=True)



# TO CREATE THE DATABASE AND TABLES 
db.create_all()