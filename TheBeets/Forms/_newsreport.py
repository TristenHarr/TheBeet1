from wtforms import Form, StringField, validators


class NewsReport(Form):
    """
    The login form built using WTForms
    """
    newslink = StringField('Article Link', [validators.InputRequired()])
