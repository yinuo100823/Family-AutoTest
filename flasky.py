from flask import render_template
from flask_login import login_required

from app import create_app

app = create_app()


@app.route("/")
@login_required
def index():
    return render_template("index.html")


if __name__ == '__main__':
    app.run()
