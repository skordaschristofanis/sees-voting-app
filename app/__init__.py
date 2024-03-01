from flask import Flask, render_template


__all__ = ['sees_voting_app']


def create_flask_app() -> Flask:
    app = Flask(__name__)

    @app.route('/')
    def vote():
        return render_template("vote.html")
    
    return app


sees_voting_app = create_flask_app()
