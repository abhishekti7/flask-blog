from flaskblog.models import User, Post
from flask import Flask, render_template, url_for, flash, redirect, request
from flaskblog.form import RegistrationForm, LoginForm
from flaskblog import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required

data = [
	{
		'title':'Blog Post 1',
		'content': 'Today was a very tiring day for me.',
		'date': '27-02-2019',
		'author':'zeus'
	},
	{
		'title':'Blog Post 2',
		'content': 'Today was a very tiring day for me.',
		'date': '27-02-2019',
		'author':'zeus'
	},
	{
		'title':'Blog Post 3',
		'content': 'Today was a very tiring day for me.',
		'date': '27-02-2019',
		'author':'zeus'
	}
]

@app.route("/")
@app.route("/home")
def home():
	return render_template('home.html')

@app.route("/about")
def display_blogs():
	return render_template("about.html",blogs=data,title="blogs")

@app.route("/contact")
def contact():
	return "Contact"

@app.route("/register",methods=["GET","POST"])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = RegistrationForm()
	if form.validate_on_submit():
		# generate password hash and create user
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user = User(username=form.username.data, email=form.email.data, password=hashed_password)
		db.session.add(user)
		db.session.commit()
		flash('Account created !','success')
		return redirect(url_for('login'))

	return render_template("register.html", title="Register", form=form)

@app.route("/login",methods=["GET","POST"])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user and bcrypt.check_password_hash(user.password, form.password.data)==True:
			login_user(user, remember=form.remember.data)
			next_page = request.args.get('next')
			return redirect(next_page) if next_page else redirect(url_for('home'))
		else:
			flash("Login unsuccessful. Check email/password",'danger')
	return render_template("login.html", title="Login", form=form)

@app.route("/forgot_password")
def forgot_password():
	return "fuck off"

@app.route("/logout")
def logout():
	logout_user()
	return redirect(url_for('home'))


@app.route("/account")
@login_required
def account():
	image_file = url_for('static', filename="img/"+current_user.image_file)
	return render_template('account.html', title='Account', image_file=image_file)
