from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from .models import User, Story, Branch
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

@main.route('/delete_story/<int:story_id>', methods=['POST'])
@login_required
def delete_story(story_id):
    story = Story.query.get_or_404(story_id)
    if story.author != current_user:
        flash('You are not authorized to delete this story.', 'error')
        return redirect(url_for('main.index'))
    db.session.delete(story)
    db.session.commit()
    flash('Story deleted successfully', 'success')
    return redirect(url_for('main.index'))

@main.route('/story/<int:story_id>/branches', methods=['GET'])
@login_required
def view_branches(story_id):
    story = Story.query.get_or_404(story_id)
    branches = story.branches
    return render_template('branches.html', story=story, branches=branches)

@main.route('/add_branch', methods=['POST'])
@login_required
def add_branch():
    content = request.form.get('content')
    story_id = request.form.get('story_id')
    if content.strip():
        new_branch = Branch(content=content, story_id=story_id)
        db.session.add(new_branch)
        db.session.commit()
        flash('Branch added successfully!', 'success')
    else:
        flash('Branch content cannot be empty.', 'error')
    return redirect(url_for('main.view_story', story_id=story_id))

@main.route('/delete_branch/<int:branch_id>', methods=['POST'])
@login_required
def delete_branch(branch_id):
    branch = Branch.query.get_or_404(branch_id)
    db.session.delete(branch)
    db.session.commit()
    flash('Branch deleted successfully', 'success')
    return redirect(url_for('main.view_branches', story_id=branch.story_id))
