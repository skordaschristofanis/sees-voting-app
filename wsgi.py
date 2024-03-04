import subprocess
from sees_voting_app import create_flask_app


app = create_flask_app()


if __name__ == "__main__":
    subprocess.run(["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "wsgi:app"])
