from flask import Blueprint, render_template, request
from podtok.models import Post

main = Blueprint('main', __name__)

@main.route("/")
def index():
    return render_template('index.html', title='Welcome to Podtok', full_width=True)

@main.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    # Query all posts
    #posts = Post.query.order_by(Post.date_posted.desc()).all()
    #users = User.query.all()  users=users, podcasts=podcasts
    #podcasts = Podcast.query.all()
    return render_template('home.html', posts=posts)

@main.route("/about")
def about():
    return render_template('about.html', title='About')