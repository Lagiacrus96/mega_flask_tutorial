from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm, RegistrationForm, EditProfileForm, EmptyForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User
from werkzeug.urls import url_parse
from datetime import datetime

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@app.route('/')             # These 2 lines are decorators
@app.route('/index')
@login_required             # Requires user to login 
def index():
    user = {'username': 'Matthew'}
    posts = [
        {
            'author': {'username': 'Robin'},
            'body': 'I love stars and shit'
        },
        {
            'author': {'username': 'Andreas'},
            'body': 'Capybara.'
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

@app.route('/user/<username>') # < > denotes dynamic component
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404() # Sends a 404 if username is not found in DB
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    form = EmptyForm()
    return render_template('user.html', user=user, posts=posts, form=form)

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash(' Your changes have been saved! ')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile',
                           form = form)

@app.route('/follow/<username>', methods=['POST'])
@login_required
def follow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash('User {} was not found! Please try again'.format(username))
            return redirect(url_for('index'))
        if user == current_user:
            flash('You cannot follow yourself!')
            return redirect(url_for('index'))
        current_user.follow(user)
        db.session.commit()
        flash('You are now following {}!'.format(username))
        return redirect(url_for('user', username=username))
    else:
        return redirect(url_for('index'))
    
@app.route('/unfollow/<username>', methods=['POST'])
@login_required
def unfollow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash('User {} was not found! Please try again.'.format(username))
            return redirect(url_for('index'))
        if user == current_user:
            flash('You cannot unfollow yourself!')
            return redirect(url_for('index'))
        current_user.unfollow(user)
        db.session.commit()
        flash('You are now unfollowing {}'.format(username))
        return redirect(url_for('user', username=username))
    else:
        return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)