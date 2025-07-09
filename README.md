# Simple Flask Backend

This repository contains a minimal Flask backend that can be deployed directly to [Render](https://render.com).

## 📦 Requirements

- Python 3.8+
- (Optional) `virtualenv` to manage dependencies locally.

## 🚀 Local Development

```bash
# 1. (Optional) create & activate virtual environment
a Python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
python app.py
```

The service will be available at `http://localhost:5000`.

## ☁️ Deployment on Render

1. Push this repository to GitHub / GitLab / Bitbucket.
2. Log in to Render and click **New > Web Service**.
3. Connect the repository.
4. Render reads `render.yaml` and pre-fills the configuration:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
5. Click **Create Web Service** and wait for the build & deploy to finish.
6. Visit the generated URL to see `{"message": "Hello from Flask on Render!"}`.

That's it! 🎉

## 🗄️ Database Setup (PostgreSQL)

The service now uses PostgreSQL (via SQLAlchemy) and expects a `DATABASE_URL` environment variable.

### Local development

1. Spin up Postgres locally (Docker example):

   ```bash
   docker run --name bitespeed-postgres -e POSTGRES_PASSWORD=secret -e POSTGRES_DB=bitespeed -p 5432:5432 -d postgres:16
   ```

2. Set the `DATABASE_URL` before running the app:

   ```bash
   export DATABASE_URL="postgresql://postgres:secret@localhost:5432/bitespeed"
   python app.py
   ```

Tables are auto-created on first run.

### Render deployment

1. Create a **PostgreSQL** service on Render.
2. In your Flask web service, go to **Environment → Add Environment Variable** and pick the database’s **Internal Database URL** as `DATABASE_URL`.
3. Redeploy. The table will be created automatically.

## 🔀 /identify Endpoint

```
POST /identify
Content-Type: application/json
{
  "email": "john@example.com",
  "phoneNumber": 1234567890
}
```

Returns:

```
{
  "contact": {
    "primaryContatctId": 1,
    "emails": ["john@example.com"],
    "phoneNumbers": ["1234567890"],
    "secondaryContactIds": []
  }
}
```

Call it with either `email`, `phoneNumber`, or both. The service merges/links duplicates based on the rules in the problem statement.
