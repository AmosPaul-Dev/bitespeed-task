from flask import Flask, jsonify
import os


def create_app():
    """Factory function to create and configure the Flask application."""
    app = Flask(__name__)

    @app.route("/")
    def index():
        """Health check / root endpoint."""
        return jsonify({"message": "Hello from Flask on Render!"})

    return app


# The WSGI-compliant app object for gunicorn/Render
app = create_app()

if __name__ == "__main__":
    # When running locally, Flask's built-in server is sufficient.
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port) 