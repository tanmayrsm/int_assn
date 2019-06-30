from flask_wtf import FlaskForm
from flask_wtf.file import FileField ,FileAllowed
from flask_login import current_user
from wtforms import StringField ,PasswordField ,SubmitField ,BooleanField ,TextAreaField
from wtforms.validators import DataRequired ,Length ,Email ,EqualTo ,ValidationError
from flaskblog.models import User ,Check


class RegistrationForm(FlaskForm):
	username = StringField('Username',
							 validators =[DataRequired(), Length(min = 2, max = 20)])
	email = StringField('Email',
							validators =[DataRequired(), Email()])
	license = StringField('License',
								validators = [DataRequired()])
	vehicle_no = StringField('Vehicle No',
								validators = [DataRequired()])

	submit = SubmitField('Add Vehicle')

	def validate_vehicle_no(self ,vehicle_no):
		user = User.query.filter_by(vehicle_no = vehicle_no.data).first()
		if user:
			raise ValidationError('Vehicle no already exixts')
	def validate_email(self ,email):
		user = User.query.filter_by(email = email.data).first()
		if user:
			raise ValidationError('Choose different email')


class LoginForm(FlaskForm):
	email = StringField('Email',
							validators =[DataRequired(), Email()])
	password = PasswordField('Password',
								validators = [DataRequired()])
	remember = BooleanField('Remember me')
	submit = SubmitField('Login')


class UpdateAccount(FlaskForm):
	username = StringField('Username',
							 validators =[DataRequired(), Length(min = 2, max = 20)])
	email = StringField('Email',
							validators =[DataRequired(), Email()])
	picture = FileField('Update Profile Pic', validators = [FileAllowed(['jpg','png','jpeg'])])

	update = SubmitField('Update Account')

	license = StringField('Username',
								validators = [DataRequired()])
	vehicle_no = StringField('Username',
								validators = [DataRequired()])


	def validate_username(self ,username):
		if username.data != current_user.username:

			user = User.query.filter_by(username = username.data).first()
			if user:
				raise ValidationError('Choose different username')
	def validate_email(self ,email):
		if email.data != current_user.email:
			user = User.query.filter_by(email = email.data).first()
			if user:
				raise ValidationError('Choose different email')

class PostForm(FlaskForm):
	vehicle_no = StringField('Vehicle no' ,validators = [DataRequired()])
	license = StringField('License' ,validators  =[DataRequired()])
	picture = FileField('Choose Pic', validators = [FileAllowed(['jpg','png','jpeg'])])

	submit = SubmitField('Authenticate')

class RequestResetForm(FlaskForm):
	email = StringField('Email',
							validators =[DataRequired(), Email()])
	submit = SubmitField('Request Password Reset')

	def validate_email(self ,email):
		user = User.query.filter_by(email = email.data).first()
		if user is None:
			raise ValidationError('Email does not exists')

class ResetPasswordForm(FlaskForm):
	password = PasswordField('Password',
								validators = [DataRequired()])
	confirm_password = PasswordField('Confirm Password',
								validators = [DataRequired(), EqualTo('password')])
	submit = SubmitField('Change password')

class SearchForm(FlaskForm):
	search = StringField('Search query.....',
							validators =[DataRequired()])
	submit = SubmitField('Search')

