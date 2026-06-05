# Milestones Tracker

A simple Flask-based milestone tracker with CRUD support.

## Features
- Add, update, and delete milestone records
- Stores dates with a fixed IST timezone
- Production-ready configuration for Render and Heroku

## Setup
1. Create and activate a Python virtual environment
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Copy environment example:
   ```bash
   cp .env.example .env
   ```
4. Run the app locally:
   ```bash
   flask run
   ```

## Deployment
### Heroku
1. Create a Heroku app
2. Set the `SECRET_KEY` and `DATABASE_URL` config vars
3. Commit and push to Heroku
4. Heroku uses the `Procfile` and `requirements.txt` automatically

### Render
1. Connect this repository to Render
2. Create a new Python Web Service
3. Use build command: `pip install -r requirements.txt`
4. Use start command: `gunicorn app:app --bind 0.0.0.0:$PORT --workers 2`
5. Add `SECRET_KEY` and `DATABASE_URL` as environment variables

## Notes
- If `DATABASE_URL` is not set, the app falls back to a local SQLite database in `instance/milestones.db`.
