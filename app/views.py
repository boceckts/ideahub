from datetime import datetime

from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user
from werkzeug.urls import url_parse

from app import app, db
from app.forms import LoginForm, RegistrationForm, NewIdeaForm, EditIdeaForm
from app.models import User, Idea


@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html", title='Home')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
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
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/leaderboard')
def leaderboard():
    return redirect(url_for('index'))
    # return render_template('leaderboard.html', title='Leaderboard')


@app.route('/newIdea', methods=['GET', 'POST'])
def newIdea():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    form = NewIdeaForm()
    if form.validate_on_submit():
        print(current_user.id)
        idea = Idea(title=form.title.data, description=form.description.data,
                    user_id=current_user.id)  # not sure if i have to initialise votes here
        db.session.add(idea)
        db.session.commit()
        flash('Your idea has been saved!')
        return redirect(url_for('index'))
    return render_template('newIdea.html', title='New Idea', form=form)


@app.route('/editIdea/<int:id>', methods=['GET', 'POST'])
def editIdea(id):
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    idea = Idea.query.filter_by(id=id).first()
    if idea:
        form = EditIdeaForm()
        if request.method == 'POST':
            idea.description = form.description.data
            idea.categories = form.categories.data
            idea.modified = datetime.utcnow()
            db.session.commit()
            flash('Your idea has been edited!')
            return redirect(url_for('ideas'))
        if request.method == 'DELETE':
            flash('Your idea has been deleted! (not working yet)')
            return redirect(url_for('ideas'))
        return render_template('editIdea.html', title='Edit Idea', form=form, idea=idea)


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    return render_template("profile.html", title='Account')


@app.route('/ideas', methods=['GET', 'POST'])
def ideas():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    ideas = Idea.query.filter_by(user_id=current_user.id)
    return render_template("ideas.html", title='Ideas', ideas=ideas)
