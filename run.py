"""Application entry point for local and containerized runs."""

from app import create_app

app = create_app()

if __name__ == "__main__":
    # Debug mode is disabled on purpose: never expose the Werkzeug debugger.
    app.run(host="0.0.0.0", port=5000, debug=False)