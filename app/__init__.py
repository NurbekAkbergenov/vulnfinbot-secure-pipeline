"""Mini-VulnFinBot application factory."""

from flask import Flask

from .routes import register_routes


def create_app(config=None):
    """Create and configure the Flask application.

    Args:
        config: optional dictionary of configuration overrides.

    Returns:
        A configured Flask application instance.
    """
    app = Flask(__name__)
    app.config.from_mapping(
        TESTING=False,
        MAX_CONTENT_LENGTH=64 * 1024,  # reject oversized request bodies early
        MAX_MESSAGE_LENGTH=1000,        # maximum allowed chat message length
        JSON_SORT_KEYS=False,
    )
    if config:
        app.config.update(config)

    register_routes(app)
    return app