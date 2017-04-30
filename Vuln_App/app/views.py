from app import app, lm, models, db
from flask import render_template, request, flash, redirect, url_for, g
from flask_login import login_user, current_user, logout_user, login_required

User = models.User
Post = models.Post
Movie = models.Movie

@app.before_request
def before_request():
    g.user = current_user

@lm.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

@app.route('/')
@app.route('/index')
def index():
	return render_template("index.html")

@app.route('/register' , methods=['GET','POST'])
def register():
	if request.method == 'POST':
		user = User(request.form['first'], request.form['last'], request.form['email'], request.form['password'])
		db.session.add(user)
		db.session.commit()
		flash('User successfully registered. Please sign in!')
		return redirect(url_for('login'))
	return render_template('register.html')
	
 
@app.route('/login', methods=['GET','POST'])
def login():
	if request.method == 'POST':
		email = request.form['email']
		password = request.form['password'] 
		sql_query = 'SELECT * FROM user where email="{}" AND password="{}"'.format(email, password)
		print(sql_query)
		result = db.session.execute(sql_query).fetchone()
		print(result)
		if not result:
			flash('Username or Password is invalid!' , 'error')
			return redirect(url_for('login'))
		registered_user = User(result[1], result[2], result[3], result[4])
		registered_user.set_id(result[0])
		#registered_user = User.query.filter_by(email=email, password=password).first()
		login_user(registered_user)
		if request.args.get('next'):
			return redirect(request.args.get('next'))
		else:
			return redirect(url_for('posts'))
	return render_template('login.html')

@app.route('/logout')
def logout():
	logout_user()
	g.user = None
	return redirect(url_for('index'))

@app.route('/forum', methods=['GET', 'POST'])
@login_required
def posts():
	if request.method == "POST":
			if current_user.get_id():
				post = Post(request.form["body"], current_user.get_id())
			else:
				post = Post(request.form["body"], -1)
			db.session.add(post)
			db.session.commit()
			return redirect(url_for('posts'))
	posts = Post.query.all()
	return render_template("forum.html", posts=reversed(posts))

@app.route('/movies', methods=["GET"])
def movies():
	try:
		if request.args.get("search"):
			#movies = Movie.query.filter(Movie.title.contains(word)).all()
			word = request.args.get("search")
			sql_query = "SELECT * FROM movie WHERE title LIKE '%{}%'".format(word)
			print(sql_query)
			result = db.session.execute(sql_query).fetchall()
			movies = []
			for movie in result:
				movies.append(Movie(movie[1], movie[2], movie[3], movie[4], movie[5]))
		else:
			movies = Movie.query.all()
	except Exception as e:
		movies = [{"title": "None",
				  "rating": "None",
				  "rated" : "None",
				  "year" : "None",
				  "genre" : "None"}]
	return render_template("movies.html", movies=movies)
