from flask import render_template
from app import app
from app.forms import LoginForm

@app.route('/')             # These 2 lines are decorators
@app.route('/index')
def index():
    user = {'username': 'Matthew'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Amsterdam!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Persona ports were so cool!'
        },
        {
            'author': {'username': 'Jesus'},
            'body': 'I have a tiny willy!'
        }
    ]
    return render_template('index.html', title='Home', user=user, posts=posts)

@app.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', title='Sign In', form=form)