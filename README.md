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
