from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from app import app, db
from app.forms import LoginForm, RegistrationForm, RequestForm
from app.models import User, Manager, Teams


@app.route('/')
@app.route('/index')
@login_required
def index():
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', title='Home', posts=posts)


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
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/request', methods=['GET'])
def request():
    form = RequestForm()
    if form.is_submitted():
        '''TODO: Query the database and route to team.html with the given team name and year'''
    return render_template('request.html', title='Request Data', form=form)


@app.route('/team', methods=['GET'])
def team(teamName, year):
    return render_template('team.html', title=teamName)


@app.route('/manager', methods=['GET'])
def team(manID):
    manName = db.session.execute(
        db.select(Manager.c.nameFirst + ' ' + Manager.c.nameLast).where(Manager.c.personId == manID)
    )
    # data = db.session.execute(
    #     db.select(Teams.c.name, Manager.c.year).join_from(
    #         Manager, Teams
    #     ).where(Manager.c.)
    # )
    return render_template('team.html', title=manName)