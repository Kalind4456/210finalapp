# app/views.py
from flask import Blueprint, render_template, request, redirect, url_for
from .models import Story, Branch
from . import db

main = Blueprint('main', __name__)

@main.route('/')
def index():
    stories = Story.query.all()
    return render_template('index.html', stories=stories)

@main.route('/story/<int:story_id>')
def view_story(story_id):
    story = Story.query.get_or_404(story_id)
    return render_template('story.html', story=story)

@main.route('/create_story', methods=['GET', 'POST'])
def create_story():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        new_story = Story(title=title, content=content)
        db.session.add(new_story)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('create_story.html')

@main.route('/delete_story/<int:story_id>', methods=['GET', 'POST'])
def delete_story(story_id):
    story = Story.query.get_or_404(story_id)
    if request.method == 'POST':
        db.session.delete(story)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('delete_story.html', story=story)

@main.route('/story/<int:story_id>/branches', methods=['GET'])
def view_branches(story_id):
    story = Story.query.get_or_404(story_id)
    branches = story.branches
    return render_template('branches.html', story=story, branches=branches)

@main.route('/add_branch', methods=['POST'])
def add_branch():
    content = request.form.get('content')
    story_id = request.form.get('story_id')
    new_branch = Branch(content=content, story_id=story_id)
    db.session.add(new_branch)
    db.session.commit()
    return redirect(url_for('main.view_story', story_id=story_id))

@main.route('/delete_branch/<int:branch_id>', methods=['POST'])
def delete_branch(branch_id):
    branch = Branch.query.get_or_404(branch_id)
    db.session.delete(branch)
    db.session.commit()
    return redirect(url_for('main.view_branches', story_id=branch.story_id))
