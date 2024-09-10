from podtok import app, db
from podtok.models import User, Post, Podcast, Episode  # Import your models

with app.app_context():
    db.create_all()
    print("Database tables created successfully.")
