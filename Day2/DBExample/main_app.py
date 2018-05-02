# An application about recording favorite songs & info

# 1:Many relationship: Album:Song(s)
# Many:Many relationship: Artists:Songs
# TODO: E-R diagram to display
# TODO: relationship to build (done, ish)
# TODO: relationship and association table to build

import os
from flask import Flask, render_template, session, redirect, url_for, flash
from flask_script import Manager, Shell
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectMultipleField
from wtforms.validators import Required
from flask_sqlalchemy import SQLAlchemy
# from flask_sqlalchemy import Table, Column, Integer, ForeignKey, String, DateTime, Date, Time
# from flask_sqlalchemy import relationship, backref

# Configure base directory of app
basedir = os.path.abspath(os.path.dirname(__file__))

# Application configurations
app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'hardtoguessstringfromsi364thisisnotsupersecurebutitsok'
app.config["SQLALCHEMY_DATABASE_URI"] = ""
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

class Album(db.Model):
    pass


class Artist(db.Model):
    pass

class Song(db.Model):
    pass

class Playlist(db.Model):
    pass


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
    return render_template('index.html', form=form)

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
