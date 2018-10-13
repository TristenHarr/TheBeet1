from flask import Flask, session, redirect, request, Response
import sqlite3
from crypotgraphy

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
