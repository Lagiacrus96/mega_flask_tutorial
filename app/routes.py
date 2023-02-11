from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User
from werkzeug.urls import url_parse

@app.route('/')             # These 2 lines are decorators
@app.route('/index')
@login_required             # Requires user to login 
def index():
    user = {'username': 'Matthew'}
    posts = [
        {
            'author': {'username': 'Robin'},
            'body': 'Beautiful day in Amsterdam!'
        },
        {
            'author': {'username': 'Andreas'},
            'body': 'The Persona ports were so cool!'
        },
        {
            'author': {'username': 'Jesus'},
            'body': 'I love Matthew!'
        }
    ]
    return render_template('index.html', title='Home', posts=posts)

@app.route('/login', methods=['GET', 'POST']) # GET requests return information to browser. POST requests give information to server
def login():
    if current_user.is_authenticated:       
        return redirect(url_from('index'))  # Fixes a small issue if a logged in user accidentally goes to /login
    form = LoginForm()
    if form.validate_on_submit(): # Will run when browser sends POST request. After all validators work, will return True
        user = User.query.filter_by(username=form.username.data).first() # filter_by returns the user object that matches username. .first() executes result
        if user is None or not user.check_password(form.password.data): # None comes from above .first()
            flash('Invalid username of password') 
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data) # Logs in the user
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)

    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations! You are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

if __name__ == "__main__":
    app.run(debug=True)