from TheBeets.conf import load_in
from flask import render_template, Response, stream_with_context, session, redirect
settings = load_in()
from TheBeets.Analysis.bayes import gimme
import pickle

from TheBeets.Forms._newsreport import NewsReport



def _reporting(request, text, text2):
    with open("/Users/trist/PyCharmProjects/TheBeet1/TheBeets/Analysis/trained.pickle", "rb") as f:
        model = pickle.load(f)
        f.close()
    pre = gimme(text.replace(".", " "), model)
    f.close()
    if pre == "Reliable":
        credibility = 100
    else:
        credibility = 0
    form = NewsReport(request.form)
    data_dict = {}
    if request.method == "POST" and form.validate():
        data_dict['newslink'] = form.newslink.data.replace("/", "`")
        return redirect("/newsreport/{}".format(data_dict["newslink"]))
    return render_template('User/reporting.html', credibility=credibility, article=pre, text2=text2)