from flask import Flask, render_template, url_for, flash, redirect, request
from forms import RegistrationForm, LoginForm
from flask_sqlalchemy import SQLAlchemy
# from audio import printWAV # Audio not used yet
import time, random, threading
from turbo_flask import Turbo
from flask_bcrypt import Bcrypt
# from flask_behind_proxy import FlaskBehindProxy #Codio solution don't want to use yet
from flask_login import UserMixin, LoginManager, login_user, logout_user, current_user, login_required

app = Flask(__name__)

app.config['SECRET_KEY'] = 'efefdc92b673d6000695ae349d5b853e'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

bcrypt = Bcrypt(app)
# turbo = Turbo(app) #might cause problems

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)


    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.password}')" 

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', subtitle='Home Page', text='This is the home page')

@app.route("/about")
def about():
    return render_template('about.html', subtitle='About', text='This is an about page')

@app.route("/youtube")
def youtube():
    return render_template('youtube.html', subtitle='Youtube',text='Info on your favorite youtuber')

@app.route("/twitch")
def twitch():
    return render_template('twitch.html', subtitle='Twitch', text='Info on your favorite streamer')

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit(): # checks if entries are valid
        passwordhash = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        username = db.session.query(User.id).filter_by(username=form.username.data).first() is not None
        if username is False:
            mail = db.session.query(User.id).filter_by(email=form.email.data).first() is not None
            if mail is False:
                user = User(username=form.username.data, email=form.email.data, password=passwordhash)
                db.session.add(user)
                db.session.commit()
                flash(f'Account created for {form.username.data}!', 'success')
                return redirect(url_for('home')) # if so - send to home page
            else:
                flash(f'That email is already taken please try another','danger')
                return redirect(url_for('register'))
        else:
            flash(f'That username is already taken please try another','danger')
            return redirect(url_for('register'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = db.session.query(User.id).filter_by(username=form.username.data).first() is not None
        if username is True:
            password = db.session.query(User.password).filter_by(username=form.username.data).first()
            password = password[0]
            if bcrypt.check_password_hash(password, form.password.data):
                remember = request.form.get('Remember') #on if checked, None if not checked
                if remember == 'on':
                    remember = True
                print(remember)
                flash(f'Logged in as {form.username.data}!', 'success')
                user = User.query.filter_by(username=form.username.data).first()
                login_user(user, remember=remember)
                return redirect(url_for('profile'))
            else:
                flash(f'Wrong password for {form.username.data}!','danger')
                return redirect(url_for('login'))
        else:
            flash(f'Account does not exist for {form.username.data}!','danger')
            return redirect(url_for('login'))
    return render_template('login.html',title='Login',form=form)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/profile")
@login_required
def profile():
    return render_template('profile.html', name=current_user.username)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash(f'Logged out', 'success')
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")