from TheBeets.conf import load_in
from flask import render_template, Response, stream_with_context, session, redirect
settings = load_in()
from TheBeets.Manager._User import User



def _newsreport(request):
        return render_template("User/newsreport.html")