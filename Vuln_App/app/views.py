from app import app, lm, models, db
from flask import render_template, request, flash, redirect, url_for, g
from flask_login import login_user, current_user, logout_user, login_required

User = models.User
Post = models.Post

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
		flash('User successfully registered')
		return redirect(url_for('login'))
	return render_template('register.html')
	
 
@app.route('/login', methods=['GET','POST'])
def login():
	if request.method == 'POST':
		email = request.form['email']
		password = request.form['password'] 
		#sql_query = 'SELECT * FROM user where email="{}" AND password="{}"'.format(email, password)
		#print(sql_query)
		registered_user = User.query.filter_by(email=email, password=password).first()
		print(registered_user)
		if registered_user is None:
			flash('Username or Password is invalid' , 'error')
			return redirect(url_for('login'))
		login_user(registered_user)
		flash('Logged in successfully')
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

@app.route('/posts', methods=['GET', 'POST'])
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
	return render_template("posts.html", posts=reversed(posts))