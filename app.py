from pathlib import Path
import os
from flask import Flask, render_template, request, redirect, url_for
from dotenv import load_dotenv
from models import db, Milestone
from config import Config
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect

load_dotenv()

migrate = Migrate()
csrf = CSRFProtect()


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)

    Path(app.instance_path).mkdir(parents=True, exist_ok=True)
    db.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)

    with app.app_context():
        db.create_all()

    @app.route('/')
    def greetings():
        milestones = Milestone.query.order_by(Milestone.id.asc()).all()
        return render_template('index.html', milestones=milestones)

    @app.route('/add', methods=['POST'])
    def add_milestone():
        title = request.form.get('title')
        description = request.form.get('description')
        if title:
            milestone = Milestone(title=title, description=description)
            db.session.add(milestone)
            db.session.commit()
        return redirect(url_for('greetings'))

    @app.route('/delete/<int:milestone_id>', methods=['POST'])
    def delete_milestone(milestone_id):
        milestone = Milestone.query.get_or_404(milestone_id)
        db.session.delete(milestone)
        db.session.commit()
        return redirect(url_for('greetings'))

    @app.route('/update/<int:milestone_id>', methods=['GET', 'POST'])
    def update_milestone(milestone_id):
        milestone = Milestone.query.get_or_404(milestone_id)
        if request.method == 'POST':
            title = request.form.get('title')
            if title:
                milestone.title = title
                milestone.description = request.form.get('description')
                milestone.date_updated = milestone.get_timestamp()
                db.session.commit()
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
