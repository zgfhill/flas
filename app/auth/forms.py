from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User

class LoginForm(FlaskForm):
	email = StringField('Email', validators=[DataRequired(), Length(1,64), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	remember_me = BooleanField('Keep me logged in')
	submit = SubmitField('Log In')

class RegistrationForm(FlaskForm):
	email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
	username = StringField('Username', validators=[DataRequired(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, 'Usernames must have only letters, numbers, dots or undersocres')])
	password = PasswordField('Password', validators=[DataRequired(), EqualTo('password2', message='Passwords must match')])
	password2 = PasswordField('confirm password', validators=[DataRequired()])
	submit = SubmitField('Register')

	def validate_email(self, field):
		if User.query.filter_by(email=field.data).first():
			raise ValidationError('Email already registered')
	
	def validate_username(self, field):
		if User.query.filter_by(username=field.data).first():
			raise ValidationError('Usernane already in use')

class ChangePasswordForm(FlaskForm):
	old_password = PasswordField('Old Password', validators=[DataRequired()])
	new_password = PasswordField('New Password', validators=[DataRequired(), EqualTo('new_password2', message='Passwords must match')])
	new_password2 = PasswordField('Confirm Password', validators=[DataRequired()])
	submit = SubmitField('提交')

class PasswordResetRequestForm(FlaskForm):
	email = StringField('Email', validators=[DataRequired(), Email()])
	submit = SubmitField('Send email')

class PasswordResetForm(FlaskForm):
	#email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('New Password', validators=[DataRequired(), EqualTo('password2', message='gun')])
	password2 = PasswordField('Password Confirm', validators=[DataRequired()])
	submit = SubmitField('改改改')

class ChangeEmailForm(FlaskForm):
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	submit = SubmitField('Change')

	def validate_email(self, field):
		if User.query.filter_by(email=field.data).first():
			raise ValidationError('Email already exist')
