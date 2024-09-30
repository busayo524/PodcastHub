from flask import Blueprint, render_template, url_for, flash, redirect, request, abort
from flask_login import current_user, login_required
from podtok import db
from podtok.models import Audio, User
from podtok.audios.forms import AudioForm
from podtok.audios.utils import save_audio

audios = Blueprint('audios', __name__)

@audios.route("/audio/new", methods=['GET', 'POST'])
@login_required
def new_audio():
    form = AudioForm()
    if form.validate_on_submit():
        audio_file = save_audio(form.audio.data)
        audio = Audio(title=form.title.data, audio_file=audio_file, author=current_user)
        db.session.add(audio)
        db.session.commit()
        flash('Your audio has been uploaded!', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_audio.html', title='New Audio', form=form, legend='New Audio')


@audios.route("/audio/upload", methods=['GET', 'POST'])
@login_required
def upload_audio():
    form = AudioForm()
    if form.validate_on_submit():
        audio_file = save_audio(form.audio.data)
        audio = Audio(title=form.title.data, audio_file=audio_file, author=current_user)
        db.session.add(audio)
        db.session.commit()
        flash('Your audio has been uploaded!', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_audio.html', title='Upload Audio', form=form, legend='Upload Audio')


@audios.route("/audio/<int:audio_id>")
def audio(audio_id):
    audio = Audio.query.get_or_404(audio_id)
    return render_template('audio.html', title=audio.title, audio=audio)

@audios.route("/audio/<int:audio_id>/update", methods=['GET', 'POST'])
@login_required
def update_audio(audio_id):
    audio = Audio.query.get_or_404(audio_id)
    if audio.author != current_user:
        abort(403)
    form = AudioForm()
    if form.validate_on_submit():
        audio.title = form.title.data
        if form.audio.data:
            audio_file = save_audio(form.audio.data)
            audio.audio_file = audio_file
        db.session.commit()
        flash('Your audio has been updated!', 'success')
        return redirect(url_for('audios.audio', audio_id=audio.id))
    elif request.method == 'GET':
        form.title.data = audio.title
    return render_template('create_audio.html', title='Update Audio', form=form, legend='Update Audio')

@audios.route("/audio/<int:audio_id>/delete", methods=['POST'])
@login_required
def delete_audio(audio_id):
    audio = Audio.query.get_or_404(audio_id)
    if audio.author != current_user:
        abort(403)
    db.session.delete(audio)
    db.session.commit()
    flash('Your audio has been deleted!', 'success')
    return redirect(url_for('main.home'))

@audios.route("/user/<string:username>/audios")
def user_audios(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    audios = Audio.query.filter_by(author=user)\
        .order_by(Audio.date_posted.desc())\
        .paginate(page=page, per_page=5)
    return render_template('user_audios.html', audios=audios, user=user)
