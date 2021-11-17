#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
from typing import ValuesView
import dateutil.parser
import babel
from flask import( 
    Flask, 
    render_template,
    request,
    Response,
    flash,
    redirect,
    url_for
)
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from models import *
from flask_migrate import Migrate

# TODO: connect to a local postgresql database - DONE

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
  # TODO: replace with real venues data.
  #       num_upcoming_shows should be aggregated based on number of upcoming shows per venue.
  
    data = []
    areas = Venue.query.distinct(Venue.city, Venue.state).all()
    
    for area in areas:
        venues = Venue.query.filter_by(city=area.city).filter_by(state=area.state).all()

        for venue in venues:
            num_upcoming_shows = Show.query.filter_by(venue_id=venue.id).order_by('id').all()
            
        data.append({
          'city': area.city,
          'state': area.state,
          'venues': [{'id': venue.id,
                'name': venue.name,
                'num_upcoming_shows': len(num_upcoming_shows)}]
        }) 
    return render_template('pages/venues.html', areas=data)

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  search_term = request.form.get('search_term', '')
  venues = Venue.query.filter(Venue.name.ilike('%' + search_term + '%')).all()
  data = []   
  for venue in venues:
      data.append({
        "name": venue.name
      })
  response={
       "data": data,
       "count": len(venues)
    }

  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue  data from the venues table, using venue_id

  venue = Venue.query.get(venue_id)
  past = db.session.query(Show).join(Artist).filter(Show.venue_id== venue_id).filter(str(Show.start_time)<str(datetime.now())).all()

  past_shows = []
  for  past_show in past:
        past_shows.append({
          "artist_id": past_show.artist_id,
          "artist_name": past_show.Artist.name,
          "artist_image_link": past_show.Artist.image_link,
          "start_time": past_show.start_time
        })

  upcoming = db.session.query(Show.artist_id,Show.start_time).filter(Show.venue_id == venue.id).filter(str(Show.start_time) >= str(datetime.now())).all()

  upcoming_shows = []
  for upcoming_show in upcoming:
        upcoming_shows.append({
          "artist_id": upcoming_show.artist_id,
          "artist_name": upcoming_show.Artist.name,
          "artist_image_link": upcoming_show.Artist.image_link,
          "start_time": upcoming_show.start_time
        })

  data = {
    "id": venue.id,
    "name": venue.name,
    "genres": venue.genres,
    "address": venue.address,
    "city": venue.city,
    "state": venue.state,  
    "phone": venue.phone,
    "website_link": venue.website_link,
    "facebook_link": venue.facebook_link,
    "seeking_talent": venue.seeking_talent,
    "seeking_description": venue.seeking_description,
    "image_link": venue.image_link,   
    "past_shows": past_shows,
    "past_shows_count": len(past_shows),
    "upcoming_shows": upcoming_shows,
    "upcoming_shows": len(upcoming_shows)
  }

  return render_template('pages/show_venue.html', venue=data)
#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  try:
      form = VenueForm(request.form)
      venue = Venue(
        name=form.name.data,
        city=form.city.data,
        state=form.state.data,
        address=form.address.data,
        phone=form.phone.data,
        genres=form.genres.data,
        facebook_link=form.facebook_link.data,
        image_link=form.image_link.data,
        website_link=form.website_link.data,
        seeking_talent=form.seeking_talent.data,
        seeking_description=form.seeking_description.data
    )
      db.session.add(venue)
      db.session.commit()
      flash('Venue: {0} created successfully'.format(venue.name))
  except Exception as err:
    flash('An error occurred creating the Venue: {0}. Error: {1}'.format(venue.name, err))
    db.session.rollback()
   # TODO: on unsuccessful db insert, flash an error instead.
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  finally:
      db.session.close()
  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  try:
    venue = Venue.query.get(Venue.id)
    db.session.delete(venue)
    db.session.commit()
  except:
    db.session.rollback()
  finally:
    db.session.close()

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return None

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  
  artists = Artist.query.all()
  data = [] 
  for artist in artists:
      data.append({
        "id": artist.id,
        "name": artist.name
      })
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  search_term = request.form.get('search_term', '') 
  artists = Artist.query.filter(Artist.name.ilike('%' + search_term + '%')).all()
  data = []   
  for artist in artists:
      data.append({
        "name": artist.name
      })
  response={
       "data": data,
        "count": len(artists)
    }

  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given artist_id
  # TODO: replace with real artist data from the artist table, using artist_id
  artist = Artist.query.get(artist_id)

  data = {
    "id": artist.id,
    "name": artist.name,
    "genres": artist.genres,
    "city": artist.city,
    "state": artist.state,  
    "phone": artist.phone,
    "facebook_link": artist.facebook_link,
    "website_link" : artist.website_link,
    "seeking_venue": artist.seeking_venue,
    "seeking_description": artist.seeking_description,
    "image_link": artist.image_link,   

  } 

  return render_template('pages/show_artist.html', artist=data)
#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  editArtist=Artist.query.filter(Artist.id == artist_id).first_or_404() #lesson 4.2
  form = ArtistForm(obj=editArtist)
    
  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=editArtist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes

  old_artist = Artist.query.filter(Artist.id == artist_id).first_or_404()
  new_artist = ArtistForm(request.form)
  error = False
  try:
        old_artist.name = new_artist.name.data,
        old_artist.city = new_artist.city.data,
        old_artist.state = new_artist.state.data,
        old_artist.phone = new_artist.phone.data,
        old_artist.genres = new_artist.genres.data,
        old_artist.image_link = new_artist.image_link.data,
        old_artist.facebook_link = new_artist.facebook_link.data,
        old_artist.website_link = new_artist.website_link.data,
        old_artist.seeking_venue = new_artist.seeking_venue.data,
        old_artist.seeking_description = new_artist.seeking_description.data

        db.session.commit()
  except:
        db.session.rollback()
  finally:
        if not error:
            flash('Artist was successfully updated!')
        else:
            flash('An error occurred. Artist could not be updated.')
        db.session.close()
  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):

  editVenue=Venue.query.filter(Venue.id == venue_id).first_or_404()
  form = VenueForm(obj=editVenue)

  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=editVenue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes

  old_venue = Venue.query.filter(Venue.id == venue_id).first_or_404()
  new_venue = VenueForm(request.form)
  error = False
  try:
        old_venue.name = new_venue.name.data,
        old_venue.city = new_venue.city.data,
        old_venue.state = new_venue.state.data,
        old_venue.phone = new_venue.phone.data,
        old_venue.genres = new_venue.genres.data,
        old_venue.image_link = new_venue.image_link.data,
        old_venue.facebook_link = new_venue .facebook_link.data,
        old_venue.website_link = new_venue.website_link.data,
        old_venue.seeking_talent = new_venue.seeking_talent.data,
        old_venue.seeking_description = new_venue.seeking_description.data

        db.session.commit()
  except:
        db.session.rollback()
  finally:
        if not error:
            flash('Venue was successfully updated!')
        else:
            flash('An error occurred. Venue could not be updated.')
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
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion

  try:
      form = ArtistForm(request.form)
      artist = Artist(
        name=form.name.data,
        city=form.city.data,
        state=form.state.data,
        phone=form.phone.data,
        genres=form.genres.data,
        image_link=form.image_link.data,
        facebook_link=form.facebook_link.data,
        website_link=form.website_link.data,
        seeking_venue=form.seeking_venue.data,
        seeking_description=form.seeking_description.data
    )
      db.session.add(artist)
      db.session.commit()
      flash('Artist: {0} created successfully'.format(artist.name))
  except Exception as err:
    flash('An error occurred creating the Venue: {0}. Error: {1}'.format(artist.name, err))
    db.session.rollback() 
  finally:
    db.session.close()    
  return render_template('pages/home.html')

#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.

  shows = Show.query.all()
  data = [] 
  for show in shows:
    data.append({
        "venue_id": show.Venue.id,
        "venue_name": show.Venue.name,
        "artist_id":show.Artist.id,
        "artist_name": show.Artist.name,
        "artist_image_link": show.Artist.image_link,
        "start_time": format_datetime(str(show.start_time))
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
  # TODO: insert form data as a new Show record in the db, instead
  try:
      form = ShowForm(request.form)
      show = Show(
        artist_id=form.artist_id.data,
        venue_id =form.venue_id.data,
        start_time=form.start_time.data
      
    )
      db.session.add(show)
      db.session.commit()
      flash('Show: {0} created successfully'.format(show.artist_id))
  except Exception as err:
    flash('An error occurred creating the Venue: {0}. Error: {1}'.format(show.artist_id, err))
    db.session.rollback() 
  finally:
    db.session.close()    
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