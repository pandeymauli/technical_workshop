# An application about recording favorite songs & info

# 1:Many relationship: Album:Song(s)
# Many:Many relationship: Artists:Songs
# TODO: E-R diagram to display
# TODO: relationship to build (done, ish)
# TODO: relationship and association table to build

import os
from flask import Flask, render_template, session, redirect, url_for, flash, request
from flask_script import Manager, Shell
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectMultipleField
from wtforms.validators import Required
from flask_sqlalchemy import SQLAlchemy
import requests
# from flask_sqlalchemy import Table, Column, Integer, ForeignKey, String, DateTime, Date, Time
# from flask_sqlalchemy import relationship, backref

# Configure base directory of app
basedir = os.path.abspath(os.path.dirname(__file__))

# Application configurations
app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'hardtoguessstringfromsi364thisisnotsupersecurebutitsok'
#app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://pandeymauli@localhost:5432/songs"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////Users/pandeymauli/UMSI/TechnicalWorkshop/Day2/DBExample/songs"
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Set up Flask debug stuff
manager = Manager(app)
# moment = Moment(app) # For time # Later
db = SQLAlchemy(app) # For database use

#########
######### Everything above this line is important/useful setup, not problem-solving.
#########

##### Set up Models #####

# Set up association Table between artists and albums
##
##

# class Album(db.Model):
#     pass


class Artist(db.Model):
    __tablename__ = 'artists'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50))
    # albums = ....
    bio = db.Column(db.String(512))

class Song(db.Model):
    __tablename__ = 'songs'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(128))
    genre = db.Column(db.String(50))
    # length = db.Column()
    artist = db.Column(db.Integer, db.ForeignKey('artists.id'))

# class Playlist(db.Model):
#     pass


##### Set up Forms #####

class SongForm(FlaskForm):
    song = StringField("What is the title of your favorite song?", validators=[Required()])
    artist = StringField("What is the name of the artist who performs it?",validators=[Required()])
    genre = StringField("What is the genre of that song?", validators
        =[Required()])
    album = StringField("What is the album this song is on?", validators
        =[Required()])
    submit = SubmitField('Submit')

class PlaylistForm(FlaskForm):
    name = StringField("What is the title of the playlist?", validators=[Required()])
    # Only creating a multiple select field, haven't initialized it yet!
    songs = SelectMultipleField("Select the songs you want to add to this playlist")
    submit = SubmitField('Submit')


##### Set up Controllers (view functions) #####

## Error handling routes
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

## Main route

@app.route('/', methods=['GET', 'POST'])
def index():
    form = SongForm()
    num_songs = len(Song.query.all())
    if request.method == 'POST':
        song = form.song.data
        genre = form.genre.data
        artist = form.artist.data
        album = form.album.data
        print(song, genre, artist, album)

        ## Created an artist object, and added it to the Aritst table
        artist_obj = Artist(name = artist, bio = '')
        db.session.add(artist_obj)
        db.session.commit()

        # Extracting the artist id so that I can use it to add the value as Forieng Key in Song table
        artist_id = artist_obj.id

        ## Created a song object, and added it to the Song table
        song_obj = Song(name = song, genre = genre, artist = artist_id)
        db.session.add(song_obj)
        db.session.commit()
        return render_template('index.html', form=form, num_songs = num_songs )
    return render_template('index.html', form=form, num_songs = num_songs )

@app.route('/all_songs')
def see_all():
    pass

@app.route('/all_artists')
def see_all_artists():
    pass

if __name__ == '__main__':
    db.create_all()
    manager.run() # NEW: run with this: python main_app.py runserver
    # Also provides more tools for debugging
