from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from form import RegistrationForm, LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = '21a00ee024ebe902cf1848208f5c1a29'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)


class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), unique=True, nullable=False)
	email = db.Column(db.String(120), unique=True, nullable=False)
	password = db.Column(db.String(60), nullable=False)
	image_file = db.Column(db.String(20),nullable=False, default='default.jpg')
	posts = db.relationship('Post',backref='author',lazy=True)

	def __repr__(self):
		return "User( '{}', '{}', '{}')".format(self.username, self.email, self.password)

class Post(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(100), nullable=False)
	date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	content = db.Column(db.Text, nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

	def __repr__(self):
		return "Post('{}', '{}')".format( self.title, self.date_posted)


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
	form = RegistrationForm()
	if form.validate_on_submit():
		flash('Account created for !','success')
		return redirect(url_for('home'))
	return render_template("register.html", title="Register", form=form)

@app.route("/login",methods=["GET","POST"])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		if form.email.data == 'abhishek.tiwari@gmail.com' and form.password.data == 'lol':
			flash("Successful Login for",'success')
			return redirect(url_for('home'))
		else:
			flash("Login unsuccessful. Check email/password",'danger')
	return render_template("login.html", title="Login", form=form)

@app.route("/forgot_password")
def forgot_password():
	return "fuck off"

if __name__ == '__main__':
	app.run(debug=True)
