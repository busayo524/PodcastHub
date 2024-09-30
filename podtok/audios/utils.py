import os
import secrets
from flask import current_app

def save_audio(audio_file):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(audio_file.filename)
    audio_fn = random_hex + f_ext
    audio_path = os.path.join(current_app.root_path, 'static/audios', audio_fn)
    audio_file.save(audio_path)
    return audio_fn