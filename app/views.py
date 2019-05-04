from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user
from werkzeug.urls import url_parse

from app import app
from app.forms import LoginForm, RegistrationForm, NewIdeaForm, EditProfileForm, EditIdeaForm
from app.models import User, Idea, Vote
from app.models.errors import VoteExistsError, IdeaNotFoundError
from app.services.idea_service import get_idea, idea_exists, delete_idea_by_id, save_idea, edit_idea, \
    get_all_ideas_for_user, get_random_unvoted_idea_for_user
from app.services.user_service import get_user_by_username, save_user, edit_user_by_form, \
    delete_user_by_id
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
        user = get_user_by_username(form.username.data)
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password', 'danger')
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
    flash('You are now logged out.', 'info')
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        save_user(user)
        flash('Congratulations, you are now a registered user!', 'info')
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
        idea = Idea(title=form.title.data,
                    description=form.description.data,
                    category=form.category.data,
                    tags=form.tags.data,
                    user_id=current_user.id)
        save_idea(idea)
        flash('Your idea has been saved!', 'info')
        return redirect(url_for('inspire'))
    return render_template('newIdea.html', title='New Idea', form=form)


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    return render_template("profile.html", title='Profile', ideas=get_all_ideas_for_user(current_user.id))


@app.route('/editProfile', methods=['GET', 'POST'])
def editProfile():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    form = EditProfileForm()
    if request.method == 'POST':
        edit_user_by_form(current_user.id, form)
        flash('Your profile has been edited!', 'info')
        return redirect(url_for('profile'))
    return render_template('editProfile.html', title='Edit Profile', form=form)


@app.route('/deleteProfile', methods=['GET'])
def deleteProfile():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    delete_user_by_id(current_user.id)
    flash('Your profile has been deleted!', 'info')
    return redirect(url_for('login'))


@app.route('/editIdea/<int:id>', methods=['GET', 'POST'])
def editIdea(id):
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    if idea_exists(id):
        form = EditIdeaForm()
        edited_idea = get_idea(id)
        if request.method == 'POST':
            edited_idea.description = form.description.data
            edited_idea.categories = form.categories.data
            edit_idea(id, edited_idea)
            flash('Your idea has been edited!', 'info')
            return redirect(url_for('profile'))
        return render_template('editIdea.html', title='Edit Idea', form=form, idea=edited_idea)


@app.route('/deleteIdea/<int:id>', methods=['GET'])
def deleteIdea(id):
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    delete_idea_by_id(id)
    flash('Your idea has been deleted!', 'info')
    return redirect(url_for('profile'))


@app.route('/inspire', methods=['GET', 'POST'])
def inspire():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    if request.method == 'POST':
        queried_idea = get_idea(request.form.get('target'))
        if queried_idea is None:
            raise IdeaNotFoundError
        if vote_exists(current_user.id, queried_idea.id):
            raise VoteExistsError
        future_vote = Vote(owner=current_user,
                           target=queried_idea,
                           value=request.form.get('value'))
        save_vote(future_vote)
    return render_template("inspire.html", title='Inspire Me', idea=get_random_unvoted_idea_for_user(current_user.id))
