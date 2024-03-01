from flask import Flask


__all__ = ['sees_voting_app']


def create_flask_app() -> Flask:
    app = Flask(__name__)

    @app.route('/')
    def home():
        return 'Hello, World!'
    
    return app


sees_voting_app = create_flask_app()
