# Deploying This App on Bluehost

## 1) Upload Code
- Upload the project files to your Bluehost Python app directory.
- Keep `passenger_wsgi.py` in the project root.

## 2) Create/Activate Python App in cPanel
- Open cPanel -> Python App.
- Create an app with the same Python version available for your plan.
- Set application root to this project folder.
- Set startup file to `passenger_wsgi.py` if prompted.

## 3) Install Dependencies
- Activate the Bluehost virtualenv from cPanel terminal.
- Run:

```bash
pip install -r requirements.txt
```

## 4) Configure Environment Variables
Set these in cPanel -> Python App -> Environment Variables:
- `FLASK_ENV=production`
- `SECRET_KEY=<long-random-secret>`
- `DATABASE_URL=<your production db url>`

Example SQLite fallback (small traffic only):
- `DATABASE_URL=sqlite:////home/<cpanel-user>/<app-folder>/app.db`

## 5) Run Migrations
From terminal (inside app root and activated venv):

```bash
export FLASK_APP=run.py
export FLASK_ENV=production
flask db upgrade
```

## 6) Restart App
- Restart from cPanel Python App panel.
- Check app URL and error logs.

## Notes
- `requirements.txt` is pinned for reproducible installs.
- `passenger_wsgi.py` imports `application` from `wsgi.py`.
- Ensure `.env`, `app.db`, and local `venv/` are not committed to remote repository.
