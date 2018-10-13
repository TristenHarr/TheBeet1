from flask import Flask, session, redirect, request, Response
import sqlite3
# from crypotgraphy import Fernet, MultiFernet
import random

from TheBeets.conf import load_in
settings = load_in()
app = Flask(__name__)
app.secret_key = bytes(random.getrandbits(16))
########################################################################################################################
#   SESSION CONFIGURATION
########################################################################################################################


def login_required():
    """
    Checks the cookie data to see if the session is new or if the user has already authenticated
    """
    if session['counter'] < 2:
        session.clear()
        return True


def sumsessioncounter():
    """
    Sums the session counter upon new page request to keep user signed in
    """
    try:
        session['counter'] += 1
    except KeyError:
        session['counter'] = 1

########################################################################################################################
# LOGIN AND REGISTER URLS
########################################################################################################################
from TheBeets.URLS.register import _register
from TheBeets.URLS.login import _login

@app.route('/', methods=["POST", "GET"])
def arrival():
    return redirect("/login")

@app.route("/login", methods=["GET", "POST"])
def login():
    """
       See URLS/login._login

       :PATH:      www.mydomain/login
       :POST:      Validates login information and redirects to /datasets
       :GET:       Renders templates/Arrival/login.html
       :return:    URLS/login._login(request)
       """
    sumsessioncounter()
    return _login(request)

@app.route('/logout')
def logout():
    """
    Clears current session and redirects to /login
    """
    session.clear()
    return redirect("/login")

@app.route('/register', methods=['POST', 'GET'])
def register():
    """
    See URLS/register._register

    :PATH:      www.mydomain/register
    :POST:      Validates form and creates a user account and redirects to /login
    :GET:       Renders templates/Arrival/signup.html
    :return:    URLS/register._register(request)
    """
    return _register(request)

########################################################################################################################
# MAIN PAGE
########################################################################################################################
from TheBeets.URLS.newsreport import _newsreport
@app.route('/newsreport', methods=['POST', 'GET'])
def newsreport():
    return _newsreport(request)


if __name__ == '__main__':
    app.run()
