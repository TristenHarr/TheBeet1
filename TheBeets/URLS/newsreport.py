from TheBeets.conf import load_in
from flask import render_template, Response, stream_with_context, session, redirect
settings = load_in()
from TheBeets.Manager._User import User
from TheBeets.Forms._newsreport import NewsReport


def _newsreport(request):
        form = NewsReport(request.form)
        data_dict = {}
        if request.method == 'POST' and form.validate():
                data_dict['newslink'] = form.newslink.data
                return redirect("/newsreport/{}".format(data_dict["newslink"]))
        return render_template("User/newsreport.html", form=form)


def _newsfetch(request, link):
        print(link)
        return redirect(link)