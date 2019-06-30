import datetime
from flaskblog import db

class User(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	username = db.Column(db.String(20), unique = True, nullable = False)
	email = db.Column(db.String(100), unique = True, nullable = False)
	image_file = db.Column(db.String(20), nullable = False ,default = 'default.jpg')
	license = db.Column(db.String(60), nullable = False)
	vehicle_no = db.Column(db.String(60), nullable = False)

	def __repr__(self):
		return f"User('{self.username}','{self.email}','{self.license}','{self.vehicle_no}')"

class Check(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	license = db.Column(db.String(100), nullable = False)
	date = db.Column(db.DateTime , nullable = False, default = datetime.datetime.now())
	vehicle_no = db.Column(db.String(100) ,nullable = False)
	image_file = db.Column(db.String(20), nullable = False ,default = 'default.jpg')
	
	def __repr__(self):
		return f"Check('{self.date}','{self.vehicle_no}','{self.license}','{self.image_file}')"
