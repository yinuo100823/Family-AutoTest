from flask import logging

from app import create_app

app = create_app()
logging = logging.create_logger(app)
# @app.route('/')
# def hello_world():
#     return 'Hello World!'


if __name__ == '__main__':
    app.run()
