from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt


app = Flask(__name__)
app.config['SECRET_KEY'] = '41d809d6415efe62514bdac2c7028143'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///podcast.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)


from podtok import routes