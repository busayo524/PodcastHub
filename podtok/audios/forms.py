from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class AudioForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    audio = FileField('Upload Audio', validators=[FileAllowed(['mp3', 'wav'])])
    submit = SubmitField('Upload')