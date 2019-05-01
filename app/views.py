from datetime import datetime

from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user
from sqlalchemy import func
from werkzeug.urls import url_parse

from app import app, db
from app.forms import LoginForm, RegistrationForm, NewIdeaForm, EditProfileForm, EditIdeaForm
from app.models import User, Idea, Vote
from app.models.errors import VoteExistsError, IdeaNotFoundError
from app.services.idea_service import get_idea
from app.services.vote_service import save_vote, vote_exists


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
        idea = Idea(title=form.title.data,
                    description=form.description.data,
                    categories=form.categories.data,
                    user_id=current_user.id)  # not sure if i have to initialise votes here
        db.session.add(idea)
        db.session.commit()
        flash('Your idea has been saved!')
        return redirect(url_for('index'))
    return render_template('newIdea.html', title='New Idea', form=form)


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    ideas = Idea.query.filter_by(user_id=current_user.id)
    return render_template("profile.html", title='Profile', ideas=ideas)


@app.route('/editProfile', methods=['GET', 'POST'])
def editProfile():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    user = User.query.filter_by(id=current_user.id).first()
    if user:
        form = EditProfileForm()
        if request.method == 'POST':
            current_user.name = form.name.data
            current_user.surname = form.surname.data
            current_user.email = form.email.data
            db.session.commit()
            flash('Your profile has been edited!')
            return redirect(url_for('profile'))
        return render_template('editProfile.html', title='Edit Profile', form=form)


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
            return redirect(url_for('profile'))
        return render_template('editIdea.html', title='Edit Idea', form=form, idea=idea)


@app.route('/deleteIdea/<int:id>', methods=['GET'])
def deleteIdea(id):
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    Idea.query.filter_by(id=id).delete()
    db.session.commit()
    flash('Your idea has been deleted!')
    return redirect(url_for('profile'))


@app.route('/voting', methods=['GET', 'POST'])
def voting():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    if request.method == 'POST':
        queried_idea = get_idea(request.form.get('target'))
        if queried_idea is None:
            raise IdeaNotFoundError
        if vote_exists(current_user.id, queried_idea.id):
            raise VoteExistsError
        future_vote = Vote.of(current_user, queried_idea, request.form.get('value'))
        save_vote(future_vote)
    rand_idea = db.session.query(Idea).filter(
        ~Idea.votes.any(Vote.user_id.is_(current_user.id))).order_by(func.random()).first()
    return render_template("voting.html", title='Voting', idea=rand_idea)
