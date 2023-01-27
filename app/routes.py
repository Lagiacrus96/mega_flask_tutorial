from flask import render_template, flash, redirect, url_for
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

@app.route('/login', methods=['GET', 'POST']) # GET requests return information to browser. POST requests give information to server
def login():
    form = LoginForm()
    if form.validate_on_submit(): # Will run when browser sends POST request. After all validators work, will return True
        flash('Login request for user {}, remember_me{}'.format( # flash is a Flask function that shows user a message
            form.username.data, form.remember_me.data))
        return redirect(url_for('/index'))

    return render_template('login.html', title='Sign In', form=form)

if __name__ == "__main__":
    app.run(debug=True)