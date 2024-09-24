import os
import secrets
from PIL import Image
from flask import url_for
from flask import current_app
from podtok import mail
from flask_mail import Message


# Define the save_picture function
def save_picture(form_picture):
    # Create a random hex filename to avoid file name conflicts
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    
    # Create the path to save the picture in your static/profile_pics directory
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)

    # Resize the image before saving it (optional, can be adjusted to your needs)
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    
    # Save the resized image to the specified path
    i.save(picture_path)
    
    return picture_fn   


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='noreply@demo.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('main.reset_token', token=token, _external=True)}

If you did not make this request, simply ignore this email and no changes will be made.
'''
    mail.send(msg)