from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from app import app, db
from app.forms import LoginForm, RegistrationForm, RequestForm
from app.models import User, Managers, Teams, People


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
        # next_page = request.args.get('next')
        # if not next_page or url_parse(next_page).netloc != '':
        #     next_page = url_for('index')
        return redirect('request')
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


@app.route('/request', methods=['GET', 'POST'])
def request():
    leagueIds = db.session.query(Teams.leagueId).distinct()
    teamNames = db.session.query(Teams.teamName).order_by(Teams.teamName.asc()).distinct()

    form = RequestForm()
    form.leagueId.choices = [l[0] for l in leagueIds]
    form.teamName.choices = [t[0] for t in teamNames]
    if form.is_submitted():
        res = db.session.query(Teams.teamId).filter_by(
            teamName=form.teamName.data,
            leagueId=form.leagueId.data,
            yr=form.year.data
        ).first()
        if res is not None:
        # print(form.leagueId.data, form.teamName.data, form.year.data)
            return redirect(f'team/{res[0]}')
    return render_template('request.html', title='Request Data', form=form)


@app.route('/team/<teamId>', methods=['GET'])
def team(teamId):
    t = db.session.query(Teams).filter_by(
        teamId=teamId
    ).first()
    if t is not None:
        managers = (db.session.query(People.firstName, People.lastName, People.personId)
                   .filter(Managers.teamId == teamId)
                   .filter(People.personId == Managers.personId
                   ).all())
        return render_template('team.html',
            title=t.teamName,
            managers=managers,
            name=t.teamName,
            rank=t.rank,
            record=(t.wins/(t.wins+t.losses)),
            year=t.yr
        )
    return render_template('team.html', name='ERROR')


@app.route('/manager/<manId>', methods=['GET'])
def manager(manId):
    manName = db.session.query(People.firstName, People.lastName).filter_by(personId=manId).first()
    teams = db.session.query(Teams.teamName, Teams.yr).filter(Teams.teamId == Managers.teamId).filter(Managers.personId == manId).all()
    return render_template('manager.html', name=(manName.firstName + ' ' + manName.lastName), teams=teams)