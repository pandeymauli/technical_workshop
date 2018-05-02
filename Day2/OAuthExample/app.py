import os
import json
import datetime

from flask import Flask, url_for, redirect, render_template, session, request, flash
from flask_sqlalchemy import SQLAlchemy
from wtforms import StringField, SubmitField, TextAreaField, IntegerField
from wtforms.validators import Required
from flask_login import LoginManager, login_required, login_user, logout_user, current_user, UserMixin
from requests_oauthlib import OAuth2Session # If you haven't, need to pip install requests_oauthlib
from requests.exceptions import HTTPError
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Shell
from flask_wtf import FlaskForm



os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1' # So you can use http, not just https
basedir = os.path.abspath(os.path.dirname(__file__))

"""App Configuration"""
## See this tutorial for how to get your application credentials and set up what you need: http://bitwiser.in/2015/09/09/add-google-login-in-flask.html
class Auth:
    """Google Project Credentials"""
    CLIENT_ID = ('REPLACE W YOUR GOOGLE CLIENT ID') # Keep the parentheses in THIS line!
    CLIENT_SECRET = 'REPLACE W YOUR CLIENT SECRET'
    REDIRECT_URI = 'http://localhost:5000/gCallback' # Our (programmer's) decision
    # URIs determined by Google, below
    AUTH_URI = 'https://accounts.google.com/o/oauth2/auth'
    TOKEN_URI = 'https://accounts.google.com/o/oauth2/token'
    USER_INFO = 'https://www.googleapis.com/userinfo/v2/me'
    SCOPE = ['profile', 'email'] # Could edit for more available scopes -- if reasonable, and possible without $$


class Config:
    """Base config"""
    APP_NAME = "Test Google Login"
    SECRET_KEY = os.environ.get("SECRET_KEY") or "something secret"


class DevConfig(Config):
    """Dev config"""
    DEBUG = True
    USE_RELOADER = True
    SQLALCHEMY_DATABASE_URI = "postgresql://localhost/oauthex2" # TODO: Need to create this database or edit URL for your computer
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True


class ProdConfig(Config):
    """Production config"""
    DEBUG = False
    USE_RELOADER = True
    SQLALCHEMY_DATABASE_URI = "postgresql://localhost/oauthex2_prod" # If you were to run a different database in production, you would put that URI here. For now, have just given a different database name, which we aren't really using.
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True

# To set up different configurations for development of an application
config = {
    "dev": DevConfig,
    "prod": ProdConfig,
    "default": DevConfig
}

"""APP creation and configuration"""
app = Flask(__name__)
app.config.from_object(config['dev']) # Here's where we specify which configuration is being used for THIS Flask application instance, stored in variable app, as usual!
db = SQLAlchemy(app)
manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)
login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.session_protection = "strong" # New - because using sessions with oauth instead of our own auth verification

## MODELS

# Association table -
to_read = db.Table('to_read',db.Column('book_id',db.Integer, db.ForeignKey('books.id')),db.Column('user_id',db.Integer, db.ForeignKey('users.id'))) # Many to many, books to users
# Of course, access current user's books with query

class Book(db.Model):
    __tablename__ = "books"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True,nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey("authors.id"))
    genre = db.Column(db.String(100))

class Author(db.Model):
    __tablename__ = "authors"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(225))
    hometown = db.Column(db.String(225)) # Assume whatever text representation is input -- e.g. 'Fairbanks, Alaska' or '105 S. State St, Ann Arbor, MI, USA', etc. All processing will be post-processing if any.
    books = db.relationship('Book',backref='Author')

class User(db.Model, UserMixin):
    __tablename__ = "users" # This was built to go with Google specific auth
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=True)
    avatar = db.Column(db.String(200))
    tokens = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    books = db.relationship('Book',secondary=to_read,backref=db.backref('books',lazy='dynamic'),lazy='dynamic')


## IMPORTANT FUNCTION / MANAGEMENT
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


""" OAuth Session creation """
def get_google_auth(state=None, token=None):
    if token:
        return OAuth2Session(Auth.CLIENT_ID, token=token)
    if state:
        return OAuth2Session(
            Auth.CLIENT_ID,
            state=state,
            redirect_uri=Auth.REDIRECT_URI)
    oauth = OAuth2Session(
        Auth.CLIENT_ID,
        redirect_uri=Auth.REDIRECT_URI,
        scope=Auth.SCOPE)
    return oauth

## FORM CLASSES

class BookEntryForm(FlaskForm):
    title = StringField("What is the title of the book?", validators=[Required()])
    author = StringField("What is the name of the author? (One author only)",validators=[Required()])
    author_hometown = StringField("What is the author's hometown?", validators=[Required()])
    submit = SubmitField("Add book to list")

## HELPER FUNCTIONS
def get_or_create_author(name, hometown):
    pass # TODO: save and return new author object if one of the same name does not already exist; if so, return that one

def get_or_create_book(book_title, author, hometown):
    pass # TODO: if not a book by this title that already exists (let's go simple for now and identify books solely by their title), save author and associate its id with the new book instance, use current_user to append the created book to the current user, and return the book object, all committed to DB

## ROUTES & VIEW FUNCTIONS

@app.route('/',methods=["GET","POST"])
@login_required
def index():
    form = BookEntryForm()
    if form.validate_on_submit():
        get_or_create_book(form.title.data,form.author.data, form.hometown.data) 
        flash("Successfully saved book, if new")
        return redirect(url_for('index'))
    return render_template('index.html',form=form)


@app.route('/all_books')
def all_books():
    books = current_user.books.all()
    return render_template('all_user_books.html',books=books)

@app.route('/login')
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    google = get_google_auth()
    auth_url, state = google.authorization_url(
        Auth.AUTH_URI, access_type='offline')
    session['oauth_state'] = state
    return render_template('login.html', auth_url=auth_url)


@app.route('/gCallback')
def callback():
    if current_user is not None and current_user.is_authenticated:
        return redirect(url_for('index'))
    if 'error' in request.args: # Good Q: 'what are request.args here, why do they matter?'
        if request.args.get('error') == 'access_denied':
            return 'You denied access.'
        return 'Error encountered.'
    # print(request.args, "ARGS")
    if 'code' not in request.args and 'state' not in request.args:
        return redirect(url_for('login'))
    else:
        google = get_google_auth(state=session['oauth_state'])
        try:
            token = google.fetch_token(
                Auth.TOKEN_URI,
                client_secret=Auth.CLIENT_SECRET,
                authorization_response=request.url)
        except HTTPError:
            return 'HTTPError occurred.'
        google = get_google_auth(token=token)
        resp = google.get(Auth.USER_INFO)
        if resp.status_code == 200:
            # print("SUCCESS 200") # For debugging/understanding
            user_data = resp.json()
            email = user_data['email']
            user = User.query.filter_by(email=email).first()
            if user is None:
                # print("No user...")
                user = User()
                user.email = email
            user.name = user_data['name']
            # print(token)
            user.tokens = json.dumps(token)
            user.avatar = user_data['picture']
            db.session.add(user)
            db.session.commit()
            login_user(user)
            return redirect(url_for('index'))
        return 'Could not fetch your information.'


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


if __name__ == "__main__":
    db.create_all()
    manager.run()
