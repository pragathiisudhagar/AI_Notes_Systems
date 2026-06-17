from flask import Blueprint, render_template, url_for, flash, redirect, request, jsonify, abort
from flask_login import login_user, current_user, logout_user, login_required
from app import db
from app.models import User, Note
from app.forms import RegistrationForm, LoginForm, NoteForm
from app.services import AIService

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return render_template('index.html')

@bp.route('/about')
def about():
    return render_template('about.html')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You can now log in.', 'success')
        return redirect(url_for('main.login'))
    return render_template('auth/register.html', title='Register', form=form)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.dashboard'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('auth/login.html', title='Login', form=form)

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@bp.route('/dashboard')
@login_required
def dashboard():
    notes = Note.query.filter_by(user_id=current_user.id).order_by(Note.updated_at.desc()).all()
    return render_template('dashboard.html', notes=notes)

@bp.route('/notes/create', methods=['GET', 'POST'])
@login_required
def create_note():
    form = NoteForm()
    if form.validate_on_submit():
        note = Note(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(note)
        db.session.commit()
        flash('Your note has been created!', 'success')
        return redirect(url_for('main.dashboard'))
    return render_template('notes/create.html', title='New Note', form=form)

@bp.route('/notes/<int:note_id>')
@login_required
def view_note(note_id):
    note = Note.query.get_or_404(note_id)
    if note.author != current_user:
        abort(403)
    return render_template('notes/view.html', title=note.title, note=note)

@bp.route('/notes/search')
@login_required
def search():
    query = request.args.get('q', '')
    if not query:
        return redirect(url_for('main.dashboard'))
    
    notes = Note.query.filter(
        Note.user_id == current_user.id,
        (Note.title.contains(query) | Note.content.contains(query))
    ).order_by(Note.updated_at.desc()).all()
    
    return render_template('notes/search.html', title='Search Results', notes=notes, query=query)

@bp.route('/notes/<int:note_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_note(note_id):
    note = Note.query.get_or_404(note_id)
    if note.author != current_user:
        abort(403)
    form = NoteForm()
    if form.validate_on_submit():
        note.title = form.title.data
        note.content = form.content.data
        db.session.commit()
        flash('Your note has been updated!', 'success')
        return redirect(url_for('main.view_note', note_id=note.id))
    elif request.method == 'GET':
        form.title.data = note.title
        form.content.data = note.content
    return render_template('notes/edit.html', title='Edit Note', form=form, note=note)

@bp.route('/notes/<int:note_id>/delete', methods=['POST'])
@login_required
def delete_note(note_id):
    note = Note.query.get_or_404(note_id)
    if note.author != current_user:
        abort(403)
    db.session.delete(note)
    db.session.commit()
    flash('Your note has been deleted.', 'success')
    return redirect(url_for('main.dashboard'))

@bp.route('/notes/<int:note_id>/summarize')
@login_required
def summarize(note_id):
    note = Note.query.get_or_404(note_id)
    if note.author != current_user:
        abort(403)
    summary = AIService.summarize_note(note.content)
    return jsonify({'result': summary})

@bp.route('/notes/<int:note_id>/key-points')
@login_required
def key_points(note_id):
    note = Note.query.get_or_404(note_id)
    if note.author != current_user:
        abort(403)
    key_points = AIService.generate_key_points(note.content)
    return jsonify({'result': key_points})

@bp.route('/notes/<int:note_id>/quiz')
@login_required
def quiz(note_id):
    note = Note.query.get_or_404(note_id)
    if note.author != current_user:
        abort(403)
    quiz_data = AIService.generate_quiz(note.content)
    return jsonify({'result': quiz_data})
