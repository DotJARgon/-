from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User, Teams
from app import db


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class RequestForm(FlaskForm):
    leagueId = SelectField('League', choices=db.session.execute(
        db.select(Teams.c.leagueId)
    ))
    teamName = SelectField('Team Name', choices=db.session.execute(
        db.select(Teams.c.teamName).where(Teams.c.leagueId == leagueId)
    ))
    year = SelectField('Year', choices=db.session.execute(
        db.select(Teams.c.yr)
        .where(Teams.c.teamName == teamName.data)
    ))
    submit = SubmitField('Submit')
