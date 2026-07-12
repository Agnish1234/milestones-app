from pathlib import Path
import logging
import os
from flask import Flask, render_template, request, redirect, url_for, flash
from dotenv import load_dotenv
from sqlalchemy.exc import SQLAlchemyError
from models import db, Milestone
from config import Config
from flask_migrate import Migrate

load_dotenv()

logger = logging.getLogger(__name__)

migrate = Migrate()


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)

    Path(app.instance_path).mkdir(parents=True, exist_ok=True)
    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        db.create_all()

    @app.route('/')
    def greetings():
        milestones = Milestone.query.order_by(Milestone.id.asc()).all()
        return render_template('index.html', milestones=milestones)

    @app.route('/add', methods=['POST'])
    def add_milestone():
        title = (request.form.get('title') or '').strip()
        description = request.form.get('description')
        if not title:
            flash('Title is required.', 'error')
            return redirect(url_for('greetings'))
        milestone = Milestone(title=title, description=description)
        db.session.add(milestone)
        try:
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            logger.exception('Failed to add milestone')
            flash('Could not save the milestone. Please try again.', 'error')
        return redirect(url_for('greetings'))

    @app.route('/delete/<int:milestone_id>', methods=['POST'])
    def delete_milestone(milestone_id):
        milestone = Milestone.query.get_or_404(milestone_id)
        db.session.delete(milestone)
        try:
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            logger.exception('Failed to delete milestone %s', milestone_id)
            flash('Could not delete the milestone. Please try again.', 'error')
        return redirect(url_for('greetings'))

    @app.route('/update/<int:milestone_id>', methods=['GET', 'POST'])
    def update_milestone(milestone_id):
        milestone = Milestone.query.get_or_404(milestone_id)
        if request.method == 'POST':
            title = (request.form.get('title') or '').strip()
            description = request.form.get('description')
            if not title:
                flash('Title is required.', 'error')
                return redirect(url_for('update_milestone', milestone_id=milestone_id))
            milestone.title = title
            milestone.description = description
            milestone.date_updated = milestone.get_timestamp()
            try:
                db.session.commit()
            except SQLAlchemyError:
                db.session.rollback()
                logger.exception('Failed to update milestone %s', milestone_id)
                flash('Could not update the milestone. Please try again.', 'error')
                return redirect(url_for('update_milestone', milestone_id=milestone_id))
            return redirect(url_for('greetings'))
        return render_template('update.html', milestone=milestone)

    @app.cli.command()
    def init_db():
        """Initialize the database."""
        db.create_all()
        print('Database initialized successfully!')

    return app


app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=os.environ.get('FLASK_DEBUG', '0') == '1')
