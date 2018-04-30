## Author : Jaclyn Cohen

## Add view functions and any other necessary code to this Flask application code below so that the routes described in the README exist and render the templates they are supposed to (all templates provided are inside the templates/ directory, where they should stay).

## As part of the homework, you may also need to add templates (new .html files) to the templates directory.

#############################
##### IMPORT STATEMENTS #####
#############################
from flask import Flask, request, render_template, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField, ValidationError
from wtforms.validators import Required

#####################
##### APP SETUP #####
#####################

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hardtoguessstring'

####################
###### WTFORMS #######
####################

# Form 1 : Lets you search for an artist
# Will need a text field and a sbumit button


####################
###### ROUTES ######
####################

@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/user/<name>')
def hello_user(name):
    return '<h1>Hello {0}<h1>'.format(name)

# Add route to display an instance of the WTForm you created above.
# You will have to use artistform.html template to render the form



# Add route to receive the data from the form and display results using artist_info.html
# Make sure you set the form action to this route in the template (artistiform.html)



if __name__ == '__main__':
    app.run(use_reloader=True,debug=True)
