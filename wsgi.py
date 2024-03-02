from sees_voting_app import create_flask_app


app = create_flask_app()


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
