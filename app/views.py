from flask import render_template, flash, redirect, url_for, request, abort
from flask_login import current_user, login_user, logout_user
from werkzeug.urls import url_parse

from app import app
from app.forms import LoginForm, RegistrationForm, NewIdeaForm, EditProfileForm, EditIdeaForm, SearchForm
from app.models import Vote
from app.models.event import EventType
from app.models.search import Search
from app.services.event_service import get_all_events_for_user
from app.services.idea_service import get_idea, idea_exists, delete_idea_by_id, get_all_ideas_for_user, \
    get_random_unvoted_idea_for_user, edit_idea_by_form, save_idea_by_form, get_ideas_by_search, get_all_ideas
from app.services.user_service import get_user_by_username, edit_user_by_form, \
    delete_user_by_id, save_user_by_form
from app.services.vote_service import save_vote, vote_exists


@app.route('/')
@app.route('/index')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    return render_template("index.html", title='Home')


@app.route('/error/<int:code>')
def error(code):
    abort(code)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        save_user_by_form(form)
        flash('Congratulations, you are now a registered user!', 'info')
        return redirect(url_for('login'))
    return render_template('authentication/register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = get_user_by_username(form.username.data)
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password', 'danger')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('home')
        return redirect(next_page)
    return render_template('authentication/login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    flash('You are now logged out.', 'info')
    return redirect(url_for('index'))


@app.route('/home')
def home():
    if not current_user.is_authenticated:
        return redirect(url_for('index'))
    return render_template("home.html", title='Home')


@app.route('/activity', methods=['GET'])
def activity():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    return render_template('events.html', title='Events', events=get_all_events_for_user(current_user.id),
                           type=EventType)


@app.route('/leaderboard')
def leaderboard():
    return redirect(url_for('home'))


@app.route('/inspire', methods=['GET', 'POST'])
def inspire():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    if request.method == 'POST':
        queried_idea = get_idea(request.form.get('target'))
        if queried_idea is None:
            abort(409)
        if vote_exists(current_user.id, queried_idea.id):
            abort(409)
        future_vote = Vote(owner=current_user,
                           target=queried_idea,
                           value=request.form.get('value'))
        save_vote(future_vote)
    return render_template("inspire.html", title='Inspire Me', idea=get_random_unvoted_idea_for_user(current_user.id))


@app.route('/user/profile', methods=['GET', 'POST'])
def profile():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    return render_template("user/show-user.html", title='Profile',
                           ideas=get_all_ideas_for_user(current_user.id))


@app.route('/user/profile/edit', methods=['GET', 'POST'])
def edit_profile():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    form = EditProfileForm(name=current_user.name,
                           surname=current_user.surname)
    if form.validate_on_submit():
        if request.method == 'POST':
            edit_user_by_form(current_user.id, form)
            flash('Your profile has been edited!', 'info')
            return redirect(url_for('profile'))
    return render_template('user/edit-user.html', title='Edit Profile', form=form)


@app.route('/user/profile/delete', methods=['GET'])
def delete_profile():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    delete_user_by_id(current_user.id)
    logout_user()
    flash('Your profile has been deleted!', 'info')
    return redirect(url_for('index'))


@app.route('/ideas/explore', methods=['GET', 'POST'])
def explore_ideas():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    form = SearchForm()
    ideas = get_all_ideas()
    if request.method == 'POST':
        ideas = get_ideas_by_search(Search.of_form(form))
    return render_template('idea/explore-ideas.html', title='Explore Ideas', form=form, ideas=ideas)


@app.route('/ideas/new', methods=['GET', 'POST'])
def create_idea():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    form = NewIdeaForm()
    if form.validate_on_submit():
        save_idea_by_form(form, current_user.id)
        flash('Your idea has been saved!', 'info')
        return redirect(url_for('inspire'))
    return render_template('idea/create-idea.html', title='New Idea', form=form)


@app.route('/ideas/<int:idea_id>/edit', methods=['GET', 'POST'])
def edit_idea(idea_id):
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    if not idea_exists(idea_id):
        abort(404)
    if current_user.id != get_idea(idea_id).author.id:
        abort(403)
    if idea_exists(idea_id):
        idea_to_edit = get_idea(idea_id)
        form = EditIdeaForm(title=idea_to_edit.title,
                            description=idea_to_edit.description,
                            category=idea_to_edit.category,
                            tags=idea_to_edit.tags)
        if form.validate_on_submit():
            if request.method == 'POST':
                edit_idea_by_form(idea_id, form)
                flash('Your idea has been edited!', 'info')
                return redirect(url_for('profile'))
        return render_template('idea/edit-idea.html', title='Edit Idea', form=form, idea=idea_to_edit)
    else:
        abort(404)


@app.route('/ideas/<int:idea_id>/delete', methods=['GET'])
def delete_idea(idea_id):
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    if not idea_exists(idea_id):
        abort(404)
    if current_user.id != get_idea(idea_id).author.id:
        abort(403)
    delete_idea_by_id(idea_id)
    flash('Your idea has been deleted!', 'info')
    return redirect(url_for('profile'))
