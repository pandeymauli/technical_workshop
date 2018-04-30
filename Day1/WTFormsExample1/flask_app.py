
## from flask.ext.wtf import Form <-- This may give you an error, depending on what
## version of flask wtf module you have installed

from flask import Flask, request, render_template, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import Required

import requests
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'

class SimpleForm(FlaskForm):
    name = StringField('Enter your email?', validators=[Required() ])
    age = IntegerField('What is your age?', validators=[ Required() ])
    submit = SubmitField('Submit')

@app.route('/')
def home():
    return "Hello, world!"

@app.route('/index') ## localhost:5000/index
def index():
    # Creating a WTForm instance
    simpleform = SimpleForm()
    return render_template('practice-form.html', form=SimpleForm)

@app.route('/result', methods = ['GET', 'POST'])
def result():
    form = NameForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        name = form.name.data
        age = form.age.data
        return "Your name is {0} and your age is {1}".format(name,age)
    flash('All fields are required!')
    return redirect(url_for('index'))
