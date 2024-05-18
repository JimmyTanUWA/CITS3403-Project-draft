from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from .models import Chat
from .forms import ChatForm
from . import db
import os
from werkzeug.utils import secure_filename

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    form = ChatForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            image_file = form.img.data
            if image_file:
                filename = secure_filename(image_file.filename)
                img_path = os.path.join('static/uploads', filename)
                image_file.save(img_path)
            else:
                img_path = None

            new_chat = Chat(data=form.data.data, img_path=img_path, user_id=current_user.id)
            db.session.add(new_chat)
            db.session.commit()
            flash('Chat added!', category='success')
            return redirect(url_for('views.home'))

    chats = Chat.query.filter_by(user_id=current_user.id).all()
    return render_template("home.html", user=current_user, form=form, chats=chats)

@views.route('/delete-chat', methods=['POST'])
@login_required
def delete_chat():
    chat_id = request.json.get('chatId')
    chat = Chat.query.get(chat_id)
    if chat and chat.user_id == current_user.id:
        db.session.delete(chat)
        db.session.commit()
        return jsonify({'success': True}), 200
    return jsonify({'error': 'Chat not found or unauthorized'}), 404

@views.route('/edit-chat/<int:chat_id>', methods=['GET', 'POST'])
@login_required
def edit_chat(chat_id):
    chat = Chat.query.get_or_404(chat_id)
    if chat.user_id != current_user.id:
        flash('Unauthorized action.', category='error')
        return redirect(url_for('views.home'))

    form = ChatForm()
    if request.method == 'POST' and form.validate_on_submit():
        chat.data = form.data.data
        image_file = form.img.data
        if image_file:
            filename = secure_filename(image_file.filename)
            img_path = os.path.join('static/uploads', filename)
            image_file.save(img_path)
            chat.img_path = img_path
        db.session.commit()
        flash('Chat updated!', category='success')
        return redirect(url_for('views.home'))

    form.data.data = chat.data
    return render_template('edit_chat.html', form=form)
