from flask import render_template, url_for, flash, redirect, request
from podtok import app, db, bcrypt
from podtok.forms import RegistrationForm, LoginForm, UpdateAccountForm
from podtok.models import User, Post, Podcast, Episode
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_login import login_user, current_user, logout_user, login_required
from PIL import Image
import os
import secrets

users = [
    {
        'id': 1,
        'username': 'adewale_vanessa',
        'email': 'adewale.vanessa@example.com',
        'password': 'hashed_password_here',
        'bio': 'Tech enthusiast and podcast host',
        'join_date': datetime(2023, 1, 15)
    },
    {
        'id': 2,
        'username': 'mary_adeoye',
        'email': 'mary.adeoye@example.com',
        'password': 'hashed_password_here',
        'bio': 'Health and wellness advocate',
        'join_date': datetime(2023, 2, 20)
    },
    {
        'id': 3,
        'username': 'tech_guru',
        'email': 'tech.guru@example.com',
        'password': 'hashed_password_here',
        'bio': 'Exploring the world of technology',
        'join_date': datetime(2023, 3, 10)
    }
]

posts = [
    {
        'id': 1,
        'user_id': 1,
        'title': 'Exciting AI Developments',
        'content': 'Just recorded a fascinating episode about the latest AI breakthroughs. Can\'t wait to share it with you all!',
        'date_posted': datetime(2023, 9, 1)
    },
    {
        'id': 2,
        'user_id': 2,
        'title': 'Meditation Challenge',
        'content': 'Starting a 30-day meditation challenge. Who wants to join me? I\'ll be sharing tips in my next podcast episode.',
        'date_posted': datetime(2023, 8, 14)
    },
    {
        'id': 3,
        'user_id': 3,
        'title': 'Tech News Roundup',
        'content': 'Here\'s a quick summary of this week\'s biggest tech news. What caught your attention?',
        'date_posted': datetime(2023, 9, 5)
    }
]

podcasts = [
    {
        'id': 1,
        'user_id': 1,
        'title': 'Tech Talk Weekly',
        'description': 'Weekly discussions on the latest in technology',
        'category': 'Technology',
        'episodes': [
            {
                'id': 1,
                'title': 'The Future of AI',
                'description': 'Exploring the latest advancements in artificial intelligence',
                'audio_file': 'path/to/future_of_ai.mp3',
                'duration': '45:00',
                'date_posted': datetime(2023, 9, 1)
            },
            {
                'id': 2,
                'title': 'Cybersecurity Essentials',
                'description': 'Tips for keeping your digital life secure',
                'audio_file': 'path/to/cybersecurity_essentials.mp3',
                'duration': '38:30',
                'date_posted': datetime(2023, 9, 8)
            }
        ]
    },
    {
        'id': 2,
        'user_id': 2,
        'title': 'Health and Wellness Journey',
        'description': 'Insights into maintaining a healthy lifestyle',
        'category': 'Health',
        'episodes': [
            {
                'id': 3,
                'title': 'Nutrition Myths Debunked',
                'description': 'Separating fact from fiction in dietary advice',
                'audio_file': 'path/to/nutrition_myths.mp3',
                'duration': '52:45',
                'date_posted': datetime(2023, 9, 11)
            },
            {
                'id': 4,
                'title': 'Mindfulness Meditation Guide',
                'description': 'A beginner\'s guide to mindfulness practices',
                'audio_file': 'path/to/mindfulness_guide.mp3',
                'duration': '40:45',
                'date_posted': datetime(2023, 8, 15)
            }
        ]
    },
    {
        'id': 3,
        'user_id': 3,
        'title': 'Tech Trends Unpacked',
        'description': 'Analyzing emerging trends in the tech industry',
        'category': 'Technology',
        'episodes': [
            {
                'id': 5,
                'title': 'The Rise of Edge Computing',
                'description': 'Understanding the shift from cloud to edge computing',
                'audio_file': 'path/to/edge_computing.mp3',
                'duration': '50:15',
                'date_posted': datetime(2023, 9, 5)
            }
        ]
    }
]


@app.route("/")
@app.route("/Home")
def home():
    return render_template('home.html', users=users, podcasts=podcasts)

@app.route("/About")
def about():
    return render_template('about.html', title='About')

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Account successfully created', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Enter a different Email or Password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/account")
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.phone_number = form.phone_number.data
        current_user.bio = form.bio.data
        current_user.dark_mode = form.dark_mode.data
        current_user.profile_pic_privacy = form.profile_pic_privacy.data
        current_user.email_notifications = form.email_notifications.data
        current_user.push_notifications = form.push_notifications.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.phone_number.data = current_user.phone_number
        form.bio.data = current_user.bio
        form.dark_mode.data = current_user.dark_mode
        form.profile_pic_privacy.data = current_user.profile_pic_privacy
        form.email_notifications.data = current_user.email_notifications
        form.push_notifications.data = current_user.push_notifications
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)