from app import db

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	first_name = db.Column(db.String(64), index=True, unique=True)
	last_name = db.Column(db.String(64), index=True, unique=True)
	email = db.Column(db.String(120), index=True, unique=True)
	password = db.Column(db.String(64), index=True, unique=True)
	posts = db.relationship('Post', backref='author', lazy='dynamic')

	def __init__(self, first, last, email, password):
		self.first_name = first
		self.last_name = last
		self.password = password
		self.email = email

	@property
	def is_authenticated(self):
		return True

	@property
	def is_active(self):
		return True

	@property
	def is_anonymous(self):
		return False

	def get_id(self):
		return str(self.id)  # python 3

	def set_id(self, num):
		self.id = num

	def __repr__(self):
		return '<User %r %r>' % (self.first_name, self.last_name)

class Post(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	body = db.Column(db.String(140))
	timestamp = db.Column(db.DateTime)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

	def __init__(self, body, user_id):
		self.body = body
		self.user_id = user_id

	def __repr__(self):
		return '<Post %r>' % (self.body)

class Movie(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	title = db.Column(db.String())
	year = db.Column(db.Integer)
	rating = db.Column(db.Integer)
	rated = db.Column(db.String())
	genre = db.Column(db.String())

	def __init__(self, title, rating, genre, rated, year, num_id=None):
		if num_id:
			self.id = num_id
		self.title = title
		self.year = year
		self.rating = rating
		self.rated = rated
		self.genre = genre

	def __repr__(self):
		return '<Title: %r Year:%r Rating:%r Rated:%r Genre:%r>' % (self.title, self.year, self.rating, self.rated, self.genre)