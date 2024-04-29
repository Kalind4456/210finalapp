from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from .models import Story
from . import db

main = Blueprint('main', __name__)

@main.route('/')
@login_required
def index():
    stories = Story.query.all()
    return render_template('index.html', stories=stories)

@main.route('/story/<int:story_id>')
@login_required
def view_story(story_id):
    story = Story.query.get_or_404(story_id)
    return render_template('story.html', story=story)

@main.route('/create_story', methods=['GET', 'POST'])
@login_required
def create_story():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        if title.strip() and content.strip():
            new_story = Story(title=title, content=content, author=current_user)
            db.session.add(new_story)
            db.session.commit()
            flash('Story created successfully!', 'success')
            return redirect(url_for('main.index'))
        else:
            flash('Title and content cannot be empty.', 'error')
    return render_template('create_story.html')

@main.route('/delete_story/<int:story_id>', methods=['GET', 'POST'])
@login_required
def delete_story(story_id):
    story = Story.query.get_or_404(story_id)
    if story.author != current_user:
        flash('You are not authorized to delete this story.', 'error')
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        db.session.delete(story)
        db.session.commit()
        flash('Story deleted successfully', 'success')
        return redirect(url_for('main.index'))

    # If the request method is GET, render the delete story confirmation page
    return render_template('delete_story.html', story=story)
