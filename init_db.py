from podtok import app, db, create_app
from podtok.models import User, Post, Podcast, Episode


app =  create_app()


with app.app_context():
    db.create_all()
    print("Database tables created successfully.")
