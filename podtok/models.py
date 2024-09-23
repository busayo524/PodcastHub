from datetime import datetime
from itsdangerous import URLSafeTimedSerializer
from flask import current_app
from podtok import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    bio = db.Column(db.Text)
    join_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    dark_mode = db.Column(db.Boolean, default=False)
    profile_pic_privacy = db.Column(db.String(20), default='public')
    notification = db.Column(db.Boolean, default=False)
    email_notifications = db.Column(db.Boolean, default=True)
    push_notifications = db.Column(db.Boolean, default=True)
    phone_number = db.Column(db.String(15), nullable=True)
    posts = db.relationship('Post', backref='author', lazy=True)
    podcasts = db.relationship('Podcast', backref='creator', lazy=True)

    def get_reset_token(self):
        s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        return s.dumps({'user_id': self.id}, salt='password-reset-salt')


    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}', '{self.bio}')"
    
    @staticmethod
    def verify_reset_token(token, expires_sec=1800):
        s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token, salt='password-reset-salt', max_age=expires_sec)['user_id']
        except:
            return None
        return User.query.get(user_id)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"Post('{self.title}', '{self.content}', '{self.date_posted}', 'Author: {self.author.username}')"
    
class Podcast(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    episode = db.relationship('Episode', backref= 'podcast', lazy=True)

    def __repr__(self):
        return f"Podcast('{self.category}', '{self.title}', '{self.episode}')"

class Episode(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    podcast_id = db.Column(db.Integer, db.ForeignKey('podcast.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    audio_file = db.Column(db.String(200), nullable=False)
    duration = db.Column(db.String(10), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"Episode('{self.title}', '{self.audio_file}', '{self.duration}', '{self.date_posted}')"
